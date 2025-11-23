# Advanced Settings Guide — NeuraHome Smart Devices
**Comprehensive Configuration for All Devices**

---

## 1. Overview
This guide covers advanced settings and configurations for all NeuraHome smart devices, including NH-Hub X1, NH-Cam Pro 360, NH-Lock Secure+, and NH-Bulb Glow RGB+.

---

## 2. NH-Hub X1 Advanced Settings

### Network Configuration
#### Ethernet Priority
1. App → **Devices → NH-Hub X1 → Settings → Network**
2. Enable **Ethernet Priority**
3. Hub uses Ethernet when available, falls back to WiFi
4. Reduces latency for critical automations

#### WiFi Band Selection
1. App → **Settings → Network → WiFi**
2. Choose **2.4 GHz Only**, **5 GHz Only**, or **Auto**
3. **2.4 GHz**: Better range, more device compatibility
4. **5 GHz**: Faster speeds, less interference
5. **Auto**: Hub selects best band automatically

#### Static IP Configuration
1. App → **Network → Advanced → Static IP**
2. Enter:
   - **IP Address** (e.g., 192.168.1.100)
   - **Subnet Mask** (usually 255.255.255.0)
   - **Gateway** (router IP, e.g., 192.168.1.1)
   - **DNS Server** (e.g., 8.8.8.8)
3. Tap **Save**
4. Hub restarts with static IP

### Device Management
#### Zigbee Channel Selection
1. App → **Hub Settings → Zigbee → Channel**
2. Choose channel **11, 15, 20, or 25**
3. Avoid channels used by WiFi (1, 6, 11)
4. Use channel scanner to find least congested

#### Device Limit Configuration
1. App → **Hub Settings → Device Limits**
2. Set maximum devices:
   - **Zigbee devices**: Up to 200
   - **WiFi devices**: Up to 50
   - **Bluetooth devices**: Up to 30
3. Hub will warn when approaching limits

#### Device Grouping
1. App → **Devices → Select Multiple Devices**
2. Tap **Group** or **Create Group**
3. Name the group (e.g., "Living Room Lights")
4. Control all devices in group simultaneously
5. Set group schedules and automations

### Automation Engine
#### Advanced Automation Rules
1. App → **Automation → Create Rule**
2. Set **Triggers**:
   - Time-based (specific time, sunrise, sunset)
   - Device state (motion detected, door opened)
   - Location (geofencing)
   - Multiple conditions (AND/OR logic)
3. Set **Actions**:
   - Control devices
   - Send notifications
   - Run scenes
   - Delay actions
4. Set **Conditions**:
   - Only if certain devices are on/off
   - Only during specific times
   - Only if no one is home

#### Automation Priorities
1. App → **Automation → Settings → Priorities**
2. Set priority levels (1-10, 1 = highest)
3. Higher priority automations run first
4. Useful for security automations (high priority)

#### Automation Logs
1. App → **Automation → Logs**
2. View automation execution history
3. See which automations ran, failed, or were skipped
4. Debug automation issues

### Security Settings
#### Local Processing Mode
1. App → **Hub Settings → Security → Local Processing**
2. Enable **Local-Only Mode**
3. All processing happens on hub (no cloud)
4. Faster response, more private
5. Requires hub to be online

#### Encryption Settings
1. App → **Security → Encryption**
2. Verify **AES-256 encryption** is enabled
3. Check **Secure Boot** status
4. Review **Certificate expiration** dates

#### Access Control
1. App → **Hub Settings → Access Control**
2. Manage who can access hub:
   - **Admin users** (full access)
   - **Standard users** (limited access)
   - **Guest users** (view only)
3. Set user permissions per device

### Performance Optimization
#### Cache Management
1. App → **Hub Settings → Performance → Cache**
2. Clear cache if hub is slow
3. Cache stores frequently accessed data
4. Automatically cleared weekly

#### Firmware Update Settings
1. App → **Hub Settings → Updates**
2. Choose update mode:
   - **Automatic** (updates at night)
   - **Manual** (you approve updates)
   - **Beta** (early access to features)
3. Set update schedule (recommended: 2-4 AM)

#### Resource Monitoring
1. App → **Hub Settings → Performance**
2. View:
   - **CPU Usage** (should be < 70%)
   - **Memory Usage** (should be < 80%)
   - **Network Traffic**
   - **Connected Devices Count**
3. Restart hub if resources are high

---

## 3. NH-Cam Pro 360 Advanced Settings

### Video Quality & Recording
#### Resolution Settings
1. App → **Camera Settings → Video → Resolution**
2. Options:
   - **2K Ultra HD** (2560×1440) - Best quality
   - **1080p Full HD** (1920×1080) - Balanced
   - **720p HD** (1280×720) - Lower bandwidth
3. Higher resolution = more storage needed

#### Frame Rate
1. App → **Video → Frame Rate**
2. Choose **30 fps** (standard) or **15 fps** (saves bandwidth)
3. 30 fps provides smoother video
4. 15 fps reduces storage and bandwidth usage

#### Recording Modes
1. App → **Camera Settings → Recording**
2. Options:
   - **Event-Only** (records when motion detected)
   - **24/7 Continuous** (records all the time)
   - **Scheduled** (records during specific times)
3. Event-only saves storage space

#### Storage Management
1. App → **Camera Settings → Storage**
2. Set **Storage Limit** (e.g., 50GB)
3. Choose **Overwrite Mode**:
   - **Oldest First** (deletes oldest videos)
   - **Stop Recording** (stops when full)
4. Enable **Cloud Backup** for important events

### Motion Detection
#### Detection Zones
1. App → **Camera Settings → Motion → Zones**
2. Draw **custom zones** on camera view
3. Camera only detects motion in selected zones
4. Reduces false alarms from trees, cars, etc.
5. Can create multiple zones

#### Sensitivity Levels
1. App → **Motion → Sensitivity**
2. Levels: **Low, Medium, High, Custom**
3. **Low**: Only large movements detected
4. **High**: Even small movements trigger alerts
5. **Custom**: Set specific thresholds

#### AI Detection Modes
1. App → **Motion → AI Detection**
2. Enable specific detection types:
   - **Person Detection** (humans only)
   - **Pet Detection** (cats, dogs)
   - **Package Detection** (deliveries)
   - **Vehicle Detection** (cars, bikes)
   - **Sound Detection** (baby crying, loud noises)
3. Reduces false alarms significantly

#### Alert Settings
1. App → **Motion → Alerts**
2. Configure:
   - **Alert Frequency** (every event, hourly summary, daily summary)
   - **Quiet Hours** (no alerts during sleep)
   - **Alert Methods** (push, email, SMS)
   - **Alert Cooldown** (wait X minutes between alerts)

### Night Vision Settings
#### IR Mode
1. App → **Camera Settings → Night Vision**
2. Choose **Auto**, **Always On**, or **Always Off**
3. **Auto**: Switches based on light level
4. **Always On**: IR LEDs always active
5. **Always Off**: Color mode only (requires some light)

#### Low-Light Color Mode
1. App → **Night Vision → Low-Light Color**
2. Enable for color video in dim light
3. Uses more power than IR mode
4. Provides color footage at night

### Privacy & Security
#### Privacy Zones
1. App → **Camera Settings → Privacy**
2. Draw zones to **block from view**
3. These areas appear black in recordings
4. Useful for windows, neighbor's property
5. Privacy zones are permanent (can't be bypassed)

#### Local Storage Encryption
1. App → **Camera Settings → Security → Encryption**
2. Enable **SD Card Encryption**
3. Videos encrypted on SD card
4. Requires password to view on other devices

#### Access Logs
1. App → **Camera Settings → Security → Access Logs**
2. View who accessed camera and when
3. See remote access attempts
4. Monitor for unauthorized access

---

## 4. NH-Lock Secure+ Advanced Settings

### Security Enhancements
#### PIN Complexity
1. App → **Lock Settings → Security → PIN Rules**
2. Enable **Strong PIN Requirement**
3. Requires:
   - Minimum 6 digits
   - Cannot be sequential (123456)
   - Cannot be repeated (111111)
   - Cannot be common patterns

#### Auto-Lock Behavior
1. App → **Lock Settings → Auto-Lock**
2. Options:
   - **Immediate** (locks as soon as door closes)
   - **Delayed** (5-30 seconds after door closes)
   - **Manual Only** (never auto-locks)
3. Set delay time if using delayed mode

#### Lockdown Mode
1. App → **Lock Settings → Security → Lockdown**
2. Configure:
   - **Failed Attempt Limit** (3-10 attempts)
   - **Lockdown Duration** (30-300 seconds)
   - **Admin Override** (admin can unlock during lockdown)
3. Prevents brute force attacks

### Access Scheduling
#### Time-Based Access
1. App → **Lock Settings → Schedules**
2. Create **time-based rules**:
   - **Work Hours** (9 AM - 5 PM weekdays)
   - **Night Mode** (10 PM - 6 AM)
   - **Weekend Schedule**
3. Users can only unlock during allowed times

#### Geofencing
1. App → **Lock Settings → Geofencing**
2. Enable **Auto-Unlock When Arriving**
3. Set **geofence radius** (50-500 meters)
4. Lock unlocks when authorized user enters area
5. Lock locks when all users leave area

### Integration Settings
#### Voice Assistant
1. App → **Lock Settings → Integrations → Voice**
2. Connect to:
   - **Amazon Alexa**
   - **Google Assistant**
   - **Apple HomeKit / Siri**
3. Enable voice commands:
   - "Alexa, lock the front door"
   - "Hey Google, unlock the door"
4. Set voice PIN for security

#### IFTTT Integration
1. App → **Lock Settings → Integrations → IFTTT**
2. Enable **IFTTT Webhooks**
3. Create applets for:
   - Lock door when leaving home
   - Unlock when arriving
   - Send notifications to other services

---

## 5. NH-Bulb Glow RGB+ Advanced Settings

### Color & Brightness
#### Color Temperature Presets
1. App → **Bulb Settings → Color → Presets**
2. Create custom color temperatures:
   - **Warm White** (2700K)
   - **Cool White** (6500K)
   - **Daylight** (5000K)
   - **Custom** (any temperature)
3. Save presets for quick access

#### Color Saturation
1. App → **Bulb Settings → Color → Saturation**
2. Adjust **color intensity** (0-100%)
3. Lower saturation = more pastel colors
4. Higher saturation = vibrant colors

#### Brightness Curves
1. App → **Bulb Settings → Brightness → Curves**
2. Set **brightness response curve**:
   - **Linear** (standard)
   - **Logarithmic** (smoother dimming)
   - **Custom** (create your own curve)
3. Improves dimming experience

### Scheduling & Automation
#### Sunrise/Sunset Schedules
1. App → **Bulb Settings → Schedules → Sun**
2. Set **Sunrise/Sunset** actions:
   - Turn on at sunset
   - Turn off at sunrise
   - Dim at specific times
3. Automatically adjusts for your location

#### Circadian Rhythm
1. App → **Bulb Settings → Health → Circadian**
2. Enable **Circadian Lighting**
3. Bulb automatically adjusts:
   - **Warmer** in evening (promotes sleep)
   - **Cooler** in morning (promotes wakefulness)
4. Based on natural light cycles

### Group Management
#### Bulb Groups
1. App → **Devices → Select Multiple Bulbs**
2. Tap **Group** or **Create Group**
3. Name group (e.g., "Living Room")
4. Control all bulbs together
5. Set group schedules and scenes

#### Scene Creation
1. App → **Scenes → Create Scene**
2. Select bulbs to include
3. Set color, brightness, temperature for each
4. Name scene (e.g., "Movie Night", "Reading")
5. Activate scene with one tap

---

## 6. App-Wide Advanced Settings

### Account Management
#### Multi-Home Support
1. App → **Settings → Homes**
2. Add multiple homes/locations
3. Switch between homes
4. Each home has separate devices
5. Useful for vacation homes, offices

#### User Roles & Permissions
1. App → **Settings → Users → Roles**
2. Assign roles:
   - **Owner** (full access)
   - **Admin** (manage devices, users)
   - **Member** (control devices)
   - **Guest** (limited access)
3. Set permissions per role

### Notifications
#### Notification Rules
1. App → **Settings → Notifications → Rules**
2. Create custom rules:
   - **Quiet Hours** (no notifications 10 PM - 7 AM)
   - **Priority Only** (only security alerts)
   - **Summary Mode** (hourly/daily summaries)
3. Filter by device type or importance

#### Notification Channels
1. App → **Settings → Notifications → Channels**
2. Configure:
   - **Push Notifications** (app alerts)
   - **Email Notifications**
   - **SMS Alerts** (for critical events)
   - **Voice Alerts** (Alexa, Google)

### Backup & Sync
#### Cloud Backup
1. App → **Settings → Backup → Cloud**
2. Enable **Automatic Cloud Backup**
3. Backup includes:
   - Device configurations
   - Automation rules
   - User settings
   - Activity logs
4. Restore from backup if needed

#### Local Backup
1. App → **Settings → Backup → Local**
2. Export settings to file
3. Save to phone storage or cloud
4. Import backup to restore settings

---

## 7. Troubleshooting Advanced Settings

### Settings Not Saving
**Solutions:**
1. Check internet connection
2. Ensure device is online
3. Restart the app
4. Clear app cache
5. Update app to latest version

### Changes Not Taking Effect
**Solutions:**
1. Wait 10-30 seconds for sync
2. Restart the device
3. Check device firmware is up to date
4. Verify settings were saved correctly
5. Contact support if issue persists

---

## 8. Support
For advanced configuration help:
- **Email:** support@neurahome.com
- **Hotline:** +1-800-NEURA-HOME
- **Advanced Support:** Available for Pro accounts

