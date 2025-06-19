import asyncio
import websockets
import json
from gesture_control import GestureController
import cv2

async def gesture_server(websocket, path):
    controller = GestureController()
    cap = cv2.VideoCapture(0)
    
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break
                
            # Process frame and get state
            processed_frame = controller.process_frame(frame)
            state = controller.get_current_state()
            
            # Send state to web client
            await websocket.send(json.dumps(state))
            
            # Show processed frame
            if processed_frame is not None:
                cv2.imshow('Gesture Control', processed_frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
                
    finally:
        cap.release()
        cv2.destroyAllWindows()

async def main():
    async with websockets.serve(
        lambda websocket: gesture_server(websocket, None), 
        "localhost", 
        8765
    ):
        await asyncio.Future()  # run forever

if __name__ == "__main__":
    asyncio.run(main())