This project is a slam based robot using intel realsense sensor to create a mobile 3-D Mapping vehicle.
It will guide you through the interfacing of fetching the point cloud data from the snesor and having an accurate postion data of the robot vehicle.
The sensor is mounted on top of the robot car .Controls for the robot is given via an online server,the imu data,point cloud data is sent from the sensor via raspberry pi which is also used for controlling our motors .
Intel real sense sensors have a poor imu data in built,hence we need a reference point of the robots positions,Which we do it by attaching optical encoders to the robots wheels.
The robot is a 6 wheel vehicle with two dummy once just rotating the encoder.
The robot only moves on 2 axis,and has tree DOF(x,y,theta)..
We must fetch the DOF datas in order to stitch the real sensor point cloud in later processing on a seperate server to recreate the 3d mapping space.
This is an ongoing project which has many problems to be solved,We are on protype one..



PROTOTYPE #1
Curently Desining the kinematics,Issues on the System,
The vehicle rotates by using slip as as a rotational motion,There are certain design aspects to be foloowed in order to achieve this.

$#In order for the vehicle to move on its center of axis..
1.The center of mass of the robot must be equal to the center of rotation.

2.The vehicle body must be symmetric,Wheels must be spaced equally on a single axis.

3.Weight must be distributed equally.

4.Tires must be having a constance coefficent of friction.

We could use an external imu sensor must must of them have less accuracy,,The encoders data cant be fetched locally on raspberry pi sue to some pull up resitor issues.hence we serially send it via arduino to pi.

#the current codes and files have been attached,.client server connections along with a script for fetching the real sense data directly from the pi .


![WhatsApp Image 2022-08-26 at 6 29 45 PM](https://user-images.githubusercontent.com/111580618/186909163-5520d5b8-51ad-486d-85f0-0621640c3ef1.jpeg)
![WhatsApp Image 2022-08-26 at 6 29 46 PM](https://user-images.githubusercontent.com/111580618/186909170-53d87aaf-2bbe-42c4-8a1a-73a7ac31caba.jpeg)
![IMG_1520](https://user-images.githubusercontent.com/111580618/186909746-07848d99-6f34-4b8f-86de-b688ed77423f.jpg)
