# MeetAttendanceScheduler
Emulator that enters and exits the Meet Room at the set time

![image](https://user-images.githubusercontent.com/35593328/103137801-a1d36780-470f-11eb-83e9-298a90e77974.png)

# Installation
1. Go to [Releases](https://github.com/Asalato/MeetAttendanceScheduler/releases) and download the . file from the latest release
1. run `MeetAttendanceScheduler.exe`

# Usage
1. (`Google Information`) Enter the email address and password of the Google account you want to sign in
1. (`Meet Room`) Enter the room ID of the Meet you want to enter
1. Enter Login time and Enter Login conditions
1. Press `Start` to start the process and `Stop` to end it (If you are in a room, you will leave the room immediately)

## Description
- Normally, it will run in the background, but you can watch it running by checking the `Show Window` checkbox
  - Set `Mute Audio` to False to hear the sound at runtime
- If you enter a time before now, you will enter/leave the room immediately
- The exit condition can be set from two options: time and the current number of people from the maximum in the room
  - The percentage is selected by moving the slider, 100% at the rightmost position, 0% at the leftmost position (Exits when the percentage drops below this level)
  - You can choose to use them both or one of them (Specify by selecting the `or` or `and` toggle)

## Load/Save Information
- Click `Save Identifier` to save the current Google account and Room ID as `identifier.txt`
- You can skip these inputs next time by loading the file from the `Load Identifier`
- If `identifier.txt` exists in the same hierarchy as the .exe file, it will be loaded automatically when the application is launched
- **In the current version, this information is stored in plain text, so please be careful when storing it (it will be encrypted in a future update)**
