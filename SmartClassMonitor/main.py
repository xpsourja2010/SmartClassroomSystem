from camera.camera_manager import CameraManager


def main():
    camera_manager = CameraManager(camera_index=0)

    try:
        camera_manager.start()

        print("SmartClassMonitor camera started.")
        print("Press Q to stop.")

        camera_manager.run()

    except Exception as error:
        print(f"Camera error: {error}")

    finally:
        camera_manager.stop()


if __name__ == "__main__":
    main()