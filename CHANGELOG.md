# Changelog

All notable changes to this project will be documented in this file.

## [1.1.0] - 2025-02-28
### Added
- **Auto-Reconnect System:** The Python logger now automatically attempts to reconnect if the Arduino is disconnected or the USB cable is unplugged.
- **Enhanced Error Handling:** Improved data validation to handle malformed serial data during reconnection.
- **Improved Logging:** Added more descriptive console messages for connection status and system startup.

### Changed
- Refactored `python/DHT22.py` to use a robust nested loop structure for continuous monitoring.
- Heartbeat thread management is now more stable, ensuring it resets properly on each new connection.

### Fixed
- Fixed an issue where the Python script would terminate immediately upon losing the serial connection.
- Fixed potential crashing when receiving incomplete data packets during reconnection.
