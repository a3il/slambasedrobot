import pyrealsense2 as rs
import numpy as np
import time
import cv2
import asyncio


class RealsenseStream:

    def __init__(self):
        print("reset start")
        ctx = rs.context()
        devices = ctx.query_devices()
        for dev in devices:
            dev.hardware_reset()
        print("reset done")
        device_id = None  # "923322071108" # serial number of device to use or None to use default
        self.enable_imu = True
        self.enable_rgb = True
        self.enable_depth = True
        # TODO: enable_pose
        # TODO: enable_ir_stereo


        # Configure streams

        self.imu_config = rs.config()
        self.imu_config.enable_stream(rs.stream.accel) # acceleration
        self.imu_config.enable_stream(rs.stream.gyro)  # gyroscope


        self.config = rs.config()
            # if we are provided with a specific device, then enable it
        if None != device_id:
            self.config.enable_device(device_id)

        self.config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 60)  # depth
        self.config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 60)  # rgb
        self.pipeline = None
        self.imu_pipeline = None
    
    def start_stream(self,queue1, queue2, event):
        try:
            print("starting streaming")
            self.pipeline = rs.pipeline()
            profile = self.pipeline.start(self.config)
            self.imu_pipeline = rs.pipeline()
            imu_profile = self.imu_pipeline.start(self.imu_config)


            # Getting the depth sensor's depth scale (see rs-align example for explanation)
            depth_sensor = profile.get_device().first_depth_sensor()
            depth_scale = depth_sensor.get_depth_scale()

            print("Depth Scale is: ", depth_scale)
                # Create an align object
                # rs.align allows us to perform alignment of depth frames to others frames
                # The "align_to" is the stream type to which we plan to align depth frames.

            align_to = rs.stream.color
            align = rs.align(align_to)	

            while True: 
                event.clear()
                frames = self.pipeline.wait_for_frames() # wait 10 seconds for first frame
                imu_frames = self.imu_pipeline.wait_for_frames()

                # Align the depth frame to color frame
                aligned_frames = align.process(frames) if self.enable_depth and self.enable_rgb else None
                depth_frame = aligned_frames.get_depth_frame() if aligned_frames is not None else frames.get_depth_frame()
                color_frame = aligned_frames.get_color_frame() if aligned_frames is not None else frames.get_color_frame()
                # Convert images to numpy arrays
                depth_image = np.asanyarray(depth_frame.get_data()) if self.enable_depth else None
                color_image = np.asanyarray(color_frame.get_data()) if self.enable_rgb else None
                depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.03), cv2.COLORMAP_JET)

                if queue1:
                    queue1.put(cv2.imencode('.png', color_image)[1].tobytes())
                if queue2:
                    queue2.put(cv2.imencode('.png', depth_colormap)[1].tobytes())
                #print("depth infromation",depth_image)
                #print("color_image",color_image)
                # Show images
                # accel_frame = imu_frames.first_or_default(rs.stream.accel, rs.format.motion_xyz32f)
                # gyro_frame = imu_frames.first_or_default(rs.stream.gyro, rs.format.motion_xyz32f)
                #print("imu \n\taccel = {}, \n\tgyro = {}".format(str(accel_frame.as_motion_frame().get_motion_data()), str(gyro_frame.as_motion_frame().get_motion_data())))
                time.sleep(0.06)
                event.wait()
        except Exception as e:
                print(e)
    
    def stop_stream(self):
        # Stop streaming
        if(self.pipeline):
            self.pipeline.stop()
        if(self.imu_pipeline):
            self.imu_pipeline.stop()
