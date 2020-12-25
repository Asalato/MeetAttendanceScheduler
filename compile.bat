call %USERPROFILE%\Anaconda3\Scripts\activate.bat
python -m eel MeetAttendanceScheduler.py web --exclude numpy --exclude pandas --onefile --noconsole
pause
exit