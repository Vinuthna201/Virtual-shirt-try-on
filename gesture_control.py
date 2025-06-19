import cv2
import mediapipe as mp
import numpy as np
from math import hypot
import os

class GestureController:
    def __init__(self):
        self.mp_pose = mp.solutions.pose
        self.mp_hands = mp.solutions.hands
        self.pose = self.mp_pose.Pose(min_detection_confidence=0.5)
        self.hands = self.mp_hands.Hands(min_detection_confidence=0.5)
        self.mp_draw = mp.solutions.drawing_utils
        
        self.frame_width = 1280
        self.frame_height = 720
        
        self.shirts = ['shirt1.png', 'shirt2.png', 'shirt3.png']
        self.current_shirt_index = 0
        self.shirt_scale = 2.0
        self.size_multiplier = 0.9
        self.prev_gesture = None
        self.gesture_cooldown = 0
        
        self.load_shirts()
    
    def load_shirts(self):
        self.shirt_images = []
        for shirt in self.shirts:
            try:
                path = os.path.join('shirts', shirt)
                img = cv2.imread(path, cv2.IMREAD_UNCHANGED)
                if img is not None:
                    self.shirt_images.append(img)
                else:
                    print(f"Failed to load image: {shirt}")
            except Exception as e:
                print(f"Error loading {shirt}: {str(e)}")

    def detect_hand_gesture(self, hand_landmarks):
        try:
            thumb_tip = hand_landmarks.landmark[4]
            index_tip = hand_landmarks.landmark[8]
            middle_tip = hand_landmarks.landmark[12]
            ring_tip = hand_landmarks.landmark[16]
            
            thumb_index_dist = hypot(thumb_tip.x - index_tip.x, thumb_tip.y - index_tip.y)
            index_middle_dist = hypot(index_tip.x - middle_tip.x, index_tip.y - middle_tip.y)
            middle_ring_dist = hypot(middle_tip.x - ring_tip.x, middle_tip.y - ring_tip.y)
            
            if self.gesture_cooldown > 0:
                self.gesture_cooldown -= 1
                return
                
            if thumb_index_dist < 0.05:
                if self.prev_gesture != 'increase':
                    self.size_multiplier = min(2.0, self.size_multiplier + 0.1)
                    self.gesture_cooldown = 10
                    self.prev_gesture = 'increase'
            elif middle_ring_dist < 0.05:
                if self.prev_gesture != 'decrease':
                    self.size_multiplier = max(0.5, self.size_multiplier - 0.1)
                    self.gesture_cooldown = 10
                    self.prev_gesture = 'decrease'
            elif index_middle_dist < 0.05:
                if self.prev_gesture != 'change':
                    self.current_shirt_index = (self.current_shirt_index + 1) % len(self.shirts)
                    self.gesture_cooldown = 10
                    self.prev_gesture = 'change'
            else:
                self.prev_gesture = None
            
        except Exception as e:
            print(f"Error in hand gesture detection: {str(e)}")

    def overlay_shirt(self, frame, landmarks):
        try:
            if not self.shirt_images:
                return frame

            left_shoulder = landmarks.landmark[self.mp_pose.PoseLandmark.LEFT_SHOULDER]
            right_shoulder = landmarks.landmark[self.mp_pose.PoseLandmark.RIGHT_SHOULDER]
            left_hip = landmarks.landmark[self.mp_pose.PoseLandmark.LEFT_HIP]
            right_hip = landmarks.landmark[self.mp_pose.PoseLandmark.RIGHT_HIP]
            
            shoulder_width = int(hypot(
                (right_shoulder.x - left_shoulder.x) * self.frame_width,
                (right_shoulder.y - left_shoulder.y) * self.frame_height
            ))
            
            torso_height = int(hypot(
                ((left_hip.x + right_hip.x)/2 - (left_shoulder.x + right_shoulder.x)/2) * self.frame_width,
                ((left_hip.y + right_hip.y)/2 - (left_shoulder.y + right_shoulder.y)/2) * self.frame_height
            ))
            
            shirt_img = self.shirt_images[self.current_shirt_index]
            shirt_width = int(shoulder_width * self.shirt_scale * self.size_multiplier)
            shirt_height = int(torso_height * 1.1)
            
            center_x = int((left_shoulder.x + right_shoulder.x) * self.frame_width / 2)
            center_y = int(left_shoulder.y * self.frame_height) - int(shirt_height * 0.13)
            
            resized_shirt = cv2.resize(shirt_img, (shirt_width, shirt_height))
            
            x1 = max(0, center_x - shirt_width // 2)
            y1 = max(0, center_y)
            x2 = min(frame.shape[1], x1 + shirt_width)
            y2 = min(frame.shape[0], y1 + shirt_height)
            
            if resized_shirt.shape[2] == 4:
                shirt_region = resized_shirt[:y2-y1, :x2-x1]
                alpha = shirt_region[:, :, 3] / 255.0
                for c in range(3):
                    frame[y1:y2, x1:x2, c] = (
                        frame[y1:y2, x1:x2, c] * (1 - alpha) +
                        shirt_region[:, :, c] * alpha
                    )
            
            return frame
        except Exception as e:
            print(f"Error in overlay_shirt: {str(e)}")
            return frame

    def process_frame(self, frame):
        try:
            if frame is None:
                return None
                
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            self.frame_height, self.frame_width = frame.shape[:2]
            
            pose_results = self.pose.process(rgb_frame)
            hands_results = self.hands.process(rgb_frame)
            
            if pose_results.pose_landmarks:
                self.mp_draw.draw_landmarks(
                    frame,
                    pose_results.pose_landmarks,
                    self.mp_pose.POSE_CONNECTIONS
                )
                
                if hands_results.multi_hand_landmarks:
                    for hand_landmarks in hands_results.multi_hand_landmarks:
                        self.mp_draw.draw_landmarks(
                            frame,
                            hand_landmarks,
                            self.mp_hands.HAND_CONNECTIONS
                        )
                        self.detect_hand_gesture(hand_landmarks)
                
                frame = self.overlay_shirt(frame, pose_results.pose_landmarks)
            
            return frame
            
        except Exception as e:
            print(f"Error in process_frame: {str(e)}")
            return frame

    def get_current_state(self):
        return {
            'current_shirt': self.shirts[self.current_shirt_index],
            'scale': int(self.size_multiplier * 100)
        }

def main():
    controller = GestureController()
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, controller.frame_width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, controller.frame_height)
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
            
        processed_frame = controller.process_frame(frame)
        if processed_frame is not None:
            state = controller.get_current_state()
            cv2.putText(
                processed_frame,
                f"Shirt: {state['current_shirt']} | Scale: {state['scale']}%",
                (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 255, 0),
                2
            )
            
            cv2.imshow('Virtual Try-On', processed_frame)
            
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()