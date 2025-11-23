# Edge Cases & Error Handling — Comprehensive Guide
**NeuraHome Systems Troubleshooting**

---

## 1. Overview
This guide covers edge cases, uncommon scenarios, and advanced error handling for all NeuraHome devices. Use this when standard troubleshooting doesn't resolve your issue.

---

## 2. NH-Hub X1 Edge Cases

### Hub Loses All Devices After Power Outage
**Symptoms:**
- Hub powers on but shows no connected devices
- Devices appear offline in app
- Automations stop working

**Causes:**
- Power outage corrupted hub memory
- Zigbee network coordinator lost
- WiFi credentials lost

**Solutions:**
1. **Soft Reset:**
   - Unplug hub for 30 seconds
   - Plug back in, wait 5 minutes
   - Check if devices reconnect automatically

2. **Re-pair Devices:**
   - App → Devices → Add Device
   - Put each device in pairing mode
   - Re-add devices one by one

3. **Network Reset:**
   - App → Hub Settings → Network → Reset
   - Re-enter WiFi password
   - Reconnect all devices

4. **Factory Reset (Last Resort):**
   - Press and hold reset button for 10 seconds
   - Hub LED flashes red
   - Reconfigure hub from scratch

### Hub Shows Connected But Devices Don't Respond
**Symptoms:**
- Hub appears online
- Devices show as connected
- Commands don't execute
- Delayed or no response

**Causes:**
- Network congestion
- Interference from other devices
- Hub overloaded with too many devices
- Firmware bug

**Solutions:**
1. **Check Hub Load:**
   - App → Hub Settings → Performance
   - If CPU > 80% or Memory > 85%, reduce devices
   - Remove unused devices

2. **Reduce Network Traffic:**
   - Disable unnecessary automations temporarily
   - Reduce automation frequency
   - Check for network loops

3. **Update Firmware:**
   - App → Hub Settings → Firmware Update
   - Install latest firmware
   - Often fixes communication bugs

4. **Restart Hub:**
   - App → Hub Settings → Restart
   - Wait 2 minutes for full restart
   - Test device control

### Hub Cannot Connect to Cloud
**Symptoms:**
- Hub works locally but cloud features fail
- Remote access doesn't work
- App shows "Hub Offline" when away
- Cloud sync errors

**Causes:**
- Internet connection issue
- Firewall blocking hub
- Cloud service outage
- DNS resolution failure

**Solutions:**
1. **Check Internet Connection:**
   - Hub Settings → Network → Test Connection
   - Verify hub can reach internet
   - Check router internet status

2. **Firewall Configuration:**
   - Allow hub IP through firewall
   - Open ports: 443 (HTTPS), 8883 (MQTT)
   - Check router firewall settings

3. **DNS Settings:**
   - Hub Settings → Network → DNS
   - Try Google DNS: 8.8.8.8, 8.8.4.4
   - Or Cloudflare DNS: 1.1.1.1, 1.0.0.1

4. **Check Cloud Status:**
   - Visit neurahome.com/status
   - Check for service outages
   - Wait if maintenance in progress

### Hub Zigbee Network Interference
**Symptoms:**
- Devices disconnect randomly
- Slow response times
- Failed commands
- Range issues

**Causes:**
- WiFi interference on same channel
- Other Zigbee networks nearby
- Physical obstructions
- Too many devices on one channel

**Solutions:**
1. **Change Zigbee Channel:**
   - Hub Settings → Zigbee → Channel
   - Use channel scanner to find best channel
   - Avoid WiFi channels (1, 6, 11)
   - Try channels 15, 20, or 25

2. **Reduce WiFi Interference:**
   - Move hub away from router
   - Use 5 GHz WiFi instead of 2.4 GHz
   - Reduce 2.4 GHz device count

3. **Add Zigbee Repeater:**
   - Install Zigbee smart plug as repeater
   - Extends network range
   - Improves signal strength

4. **Reposition Hub:**
   - Place hub centrally in home
   - Avoid metal enclosures
   - Keep away from large appliances

---

## 3. NH-Cam Pro 360 Edge Cases

### Camera Records But Shows Black Screen
**Symptoms:**
- Camera appears online
- Recording indicator active
- Playback shows black screen
- No video feed in app

**Causes:**
- Lens cap or obstruction
- IR filter stuck
- Sensor failure
- Firmware corruption

**Solutions:**
1. **Check Physical Obstructions:**
   - Remove any lens cap
   - Clean lens with microfiber cloth
   - Check for stickers or covers

2. **Reset IR Filter:**
   - App → Camera Settings → Night Vision → Reset
   - Toggle night vision on/off
   - Restart camera

3. **Firmware Recovery:**
   - App → Camera Settings → Firmware → Recovery Mode
   - Reinstall firmware
   - May require manual update via USB

4. **Hardware Check:**
   - If all software fixes fail, likely sensor issue
   - Contact support for replacement
   - Check warranty status

### Camera Motion Detection Too Sensitive
**Symptoms:**
- Constant motion alerts
- False alarms from shadows, trees, cars
- Too many notifications
- Storage filling up quickly

**Causes:**
- Sensitivity set too high
- No detection zones configured
- AI detection not enabled
- Environmental factors (wind, lighting)

**Solutions:**
1. **Adjust Sensitivity:**
   - Camera Settings → Motion → Sensitivity → Low
   - Test for 24 hours
   - Increase gradually if needed

2. **Set Detection Zones:**
   - Camera Settings → Motion → Zones
   - Draw zones only where motion matters
   - Exclude trees, roads, neighbor's property

3. **Enable AI Detection:**
   - Camera Settings → Motion → AI Detection
   - Enable "Person Detection Only"
   - Reduces false alarms significantly

4. **Environmental Adjustments:**
   - Reposition camera to avoid moving objects
   - Adjust camera angle
   - Add physical barriers (fence, plants)

### Camera SD Card Errors
**Symptoms:**
- "SD Card Error" message
- Recordings not saving
- Card not detected
- Corrupted files

**Causes:**
- SD card incompatible
- Card corrupted
- Card full
- Card speed too slow
- Physical damage

**Solutions:**
1. **Check Card Compatibility:**
   - Use Class 10 or UHS-I cards
   - Minimum 32GB, recommended 64-256GB
   - Format: FAT32 or exFAT
   - Avoid no-name brands

2. **Format SD Card:**
   - Remove card from camera
   - Format on computer (FAT32)
   - Reinsert and format in app
   - App → Camera Settings → Storage → Format

3. **Check Card Health:**
   - Test card in computer
   - Run disk check utility
   - Replace if errors found

4. **Replace Card:**
   - Use high-quality SD card
   - SanDisk, Samsung, or Kingston recommended
   - Avoid used or refurbished cards

### Camera Night Vision Not Working
**Symptoms:**
- Black and white video at night
- No IR illumination
- Poor night vision quality
- IR LEDs not turning on

**Causes:**
- IR LEDs failed
- IR filter stuck
- Settings misconfigured
- Low light mode enabled incorrectly

**Solutions:**
1. **Check IR Settings:**
   - Camera Settings → Night Vision → Mode
   - Set to "Auto" or "Always On"
   - Disable "Low-Light Color" if IR not working

2. **Test IR LEDs:**
   - Cover camera lens with hand
   - Look for red glow from IR LEDs
   - If no glow, LEDs may be failed

3. **Reset Night Vision:**
   - Toggle night vision off/on
   - Restart camera
   - Update firmware

4. **Hardware Replacement:**
   - If IR LEDs failed, contact support
   - May require camera replacement
   - Check warranty coverage

---

## 4. NH-Lock Secure+ Edge Cases

### Lock Unlocks But Doesn't Lock
**Symptoms:**
- Unlock works normally
- Lock command doesn't work
- Auto-lock not functioning
- Manual lock via keypad fails

**Causes:**
- Motor mechanism issue
- Deadbolt alignment problem
- Low battery
- Mechanical obstruction

**Solutions:**
1. **Check Battery:**
   - Replace batteries (even if not low)
   - Use high-quality alkaline batteries
   - Check battery orientation

2. **Test Manual Lock:**
   - Try locking with physical key
   - If key works, issue is electronic
   - If key doesn't work, mechanical issue

3. **Check Deadbolt Alignment:**
   - Open door and check strike plate
   - Deadbolt should align with hole
   - Adjust strike plate if misaligned

4. **Motor Reset:**
   - Remove batteries for 30 seconds
   - Reinsert batteries
   - Try lock command again
   - May need motor replacement if persists

### Lock Shows "Offline" But Works Locally
**Symptoms:**
- Lock works with keypad and app locally
- Shows "Offline" in app
- Remote unlock doesn't work
- No cloud connectivity

**Causes:**
- WiFi connection lost
- Router blocking lock
- Cloud sync issue
- Lock WiFi module issue

**Solutions:**
1. **Check WiFi Connection:**
   - Lock Settings → Network → Test Connection
   - Verify lock can reach router
   - Check signal strength (should be > -70 dBm)

2. **Reconnect WiFi:**
   - Lock Settings → Network → WiFi → Reconnect
   - Re-enter WiFi password
   - Wait 2 minutes for connection

3. **Router Configuration:**
   - Ensure 2.4 GHz WiFi enabled
   - Check MAC filtering (add lock MAC if enabled)
   - Verify router not blocking device

4. **Reset Network:**
   - Lock Settings → Network → Reset
   - Re-pair lock to WiFi
   - May require re-adding lock in app

### Lock Fingerprint Recognition Fails After Working
**Symptoms:**
- Fingerprint worked before
- Now fails consistently
- Other fingerprints work
- Specific finger not recognized

**Causes:**
- Fingerprint sensor dirty
- Finger condition changed (dry, wet, injured)
- Sensor calibration drift
- Too many failed attempts

**Solutions:**
1. **Clean Sensor:**
   - Use microfiber cloth
   - Gently wipe sensor surface
   - Avoid chemicals or water
   - Dry completely before use

2. **Re-enroll Fingerprint:**
   - App → User Management → Select User
   - Remove old fingerprint
   - Re-enroll same finger
   - Enroll multiple times for better accuracy

3. **Try Different Finger:**
   - Enroll index finger instead of thumb
   - Index fingers often work better
   - Enroll both index fingers

4. **Check Finger Condition:**
   - Ensure finger is clean and dry
   - Avoid using if finger is injured
   - Moisturize if skin is very dry
   - Wait if finger is wet

### Lock Auto-Lock Not Working
**Symptoms:**
- Door closes but doesn't auto-lock
- Auto-lock delay not functioning
- Manual lock required every time

**Causes:**
- Auto-lock disabled
- Delay set too long
- Door sensor not detecting close
- Mechanical issue

**Solutions:**
1. **Check Auto-Lock Settings:**
   - Lock Settings → Auto-Lock → Enable
   - Set delay (5-30 seconds recommended)
   - Test with door close

2. **Verify Door Sensor:**
   - Lock should detect door position
   - Check if door fully closes
   - Adjust door if needed

3. **Test Auto-Lock:**
   - Close door and wait
   - Watch lock LED (should flash then lock)
   - If no response, sensor may be faulty

4. **Manual Override:**
   - Use manual lock (hold * for 2 seconds)
   - Or lock via app
   - Contact support if auto-lock hardware failed

---

## 5. NH-Bulb Glow RGB+ Edge Cases

### Bulb Changes Color Randomly
**Symptoms:**
- Bulb changes color without command
- Color doesn't match app setting
- Random color changes
- Inconsistent behavior

**Causes:**
- Automation interfering
- Group control conflict
- Firmware bug
- WiFi interference

**Solutions:**
1. **Check Automations:**
   - App → Automation → Review Rules
   - Disable automations affecting bulb
   - Check for conflicting rules

2. **Remove from Groups:**
   - App → Devices → Bulb → Groups
   - Remove from all groups
   - Test bulb individually

3. **Reset Bulb:**
   - Turn bulb off/on 5 times quickly
   - Bulb flashes white (reset mode)
   - Re-add bulb in app
   - Reconfigure settings

4. **Update Firmware:**
   - App → Bulb Settings → Firmware Update
   - Install latest firmware
   - Often fixes color control bugs

### Bulb Not Responding to Voice Commands
**Symptoms:**
- Bulb works in app
- Voice commands don't work
- Alexa/Google doesn't control bulb
- "Device not found" errors

**Causes:**
- Voice assistant not linked
- Bulb name conflicts
- Integration disabled
- Cloud sync issue

**Solutions:**
1. **Re-link Voice Assistant:**
   - App → Bulb Settings → Integrations → Voice
   - Disconnect and reconnect Alexa/Google
   - Re-authorize permissions

2. **Check Bulb Name:**
   - Use simple names (avoid special characters)
   - Rename if name is too long
   - Avoid duplicate names

3. **Enable Integration:**
   - Verify integration is enabled
   - Check account linking status
   - Re-sync devices to voice assistant

4. **Cloud Sync:**
   - App → Settings → Sync → Force Sync
   - Wait 2 minutes
   - Try voice command again

### Bulb Flickers or Stutters
**Symptoms:**
- Bulb flickers when on
- Dimming causes stuttering
- Inconsistent brightness
- Random flashing

**Causes:**
- Incompatible dimmer switch
- WiFi signal weak
- Power supply issue
- Bulb hardware fault

**Solutions:**
1. **Check Dimmer Switch:**
   - Smart bulbs don't work with traditional dimmers
   - Replace dimmer with regular switch
   - Or use smart dimmer switch

2. **Improve WiFi Signal:**
   - Move router closer to bulb
   - Add WiFi extender
   - Check signal strength in app

3. **Power Supply:**
   - Ensure proper voltage (100-240V)
   - Check for power fluctuations
   - Use surge protector

4. **Hardware Test:**
   - Try bulb in different socket
   - If flickering persists, bulb may be faulty
   - Contact support for replacement

---

## 6. General Edge Cases

### Multiple Devices Offline Simultaneously
**Symptoms:**
- Several devices go offline at once
- Hub still online
- Network appears fine
- Affects multiple device types

**Causes:**
- Router restart or firmware update
- Network-wide power outage
- ISP internet outage
- Router configuration change

**Solutions:**
1. **Check Router Status:**
   - Verify router is online
   - Check router admin panel
   - Restart router if needed

2. **Wait for Auto-Reconnect:**
   - Devices usually reconnect automatically
   - Wait 5-10 minutes
   - Check app for reconnection

3. **Manual Reconnect:**
   - App → Devices → Select Offline Device
   - Tap "Reconnect" or "Refresh"
   - Re-enter WiFi password if prompted

4. **Network Reset:**
   - If many devices offline, reset network
   - Reconfigure router settings
   - Re-add devices if necessary

### App Shows Wrong Device Status
**Symptoms:**
- App shows device on but it's off
- Status doesn't update
- Controls don't match reality
- Sync issues

**Causes:**
- Cloud sync delay
- Local cache issue
- Device not reporting status
- App bug

**Solutions:**
1. **Refresh App:**
   - Pull down to refresh device list
   - Or close and reopen app
   - Wait for status update

2. **Clear App Cache:**
   - Phone Settings → Apps → NeuraHome → Clear Cache
   - Restart app
   - Status should update

3. **Force Sync:**
   - App → Settings → Sync → Force Sync
   - Wait for sync to complete
   - Check device status

4. **Restart Device:**
   - Power cycle the device
   - Device will report correct status
   - App should update

### Firmware Update Fails
**Symptoms:**
- Update starts but fails
- Device stuck in update mode
- Error messages during update
- Device becomes unresponsive

**Causes:**
- Internet connection lost during update
- Low battery/power
- Insufficient storage
- Corrupted firmware file

**Solutions:**
1. **Check Prerequisites:**
   - Ensure device battery > 40%
   - Verify stable internet connection
   - Check available storage space

2. **Retry Update:**
   - Wait 10 minutes
   - Retry firmware update
   - Often works on second attempt

3. **Recovery Mode:**
   - For hub: Hold reset button during power-on
   - For other devices: Follow device-specific recovery
   - Reinstall firmware manually

4. **Contact Support:**
   - If device stuck, contact support immediately
   - May need replacement if recovery fails
   - Check warranty status

---

## 7. Error Code Reference

### Hub Error Codes
| Code | Meaning | Solution |
|------|---------|----------|
| H101 | Zigbee coordinator lost | Reset Zigbee network |
| H202 | WiFi connection failed | Reconnect WiFi |
| H303 | Cloud sync error | Check internet, retry sync |
| H404 | Device limit reached | Remove unused devices |
| H505 | Firmware update failed | Retry update, use recovery mode |

### Camera Error Codes
| Code | Meaning | Solution |
|------|---------|----------|
| C101 | WiFi password wrong | Re-enter password |
| C202 | No internet connection | Check router |
| C308 | SD card not detected | Reinsert or reformat card |
| C401 | Motor rotation blocked | Remove obstruction |
| C509 | Cloud sync error | Re-login to account |
| C610 | Night vision failed | Check IR LEDs, reset |

### Lock Error Codes
| Code | Meaning | Solution |
|------|---------|----------|
| E01 | Fingerprint sensor error | Clean sensor, retry |
| E02 | Motor jam | Check alignment |
| E03 | Network connection failed | Reconnect WiFi |
| E04 | Low battery | Replace batteries |
| E05 | Incorrect PIN attempts exceeded | Wait 60 seconds |
| E06 | Firmware update failed | Retry in app |
| E07 | Deadbolt misaligned | Adjust strike plate |
| E08 | Auto-lock sensor failed | Check door sensor |

### Bulb Error Codes
| Code | Meaning | Solution |
|------|---------|----------|
| B101 | WiFi connection lost | Reconnect to network |
| B202 | Color calibration failed | Reset bulb |
| B303 | Dimmer incompatible | Remove dimmer switch |
| B404 | Group sync error | Remove from group, re-add |

---

## 8. Advanced Recovery Procedures

### Factory Reset Procedures

#### Hub Factory Reset
1. Unplug hub from power
2. Press and hold reset button
3. While holding, plug in power
4. Continue holding for 10 seconds
5. LED flashes red rapidly
6. Release button
7. Wait 5 minutes for reset
8. Reconfigure hub from scratch

#### Lock Factory Reset
1. Remove batteries
2. Press and hold `*` and `#` simultaneously
3. While holding, reinsert batteries
4. Continue holding for 10 seconds
5. Keypad flashes all colors
6. Release buttons
7. Lock resets to factory defaults

#### Camera Factory Reset
1. Power off camera
2. Press and hold reset button (usually inside)
3. While holding, power on camera
4. Continue holding for 15 seconds
5. LED flashes yellow rapidly
6. Release button
7. Camera resets (requires re-pairing)

#### Bulb Factory Reset
1. Turn bulb on
2. Turn off/on 5 times quickly (within 5 seconds)
3. Bulb flashes white 3 times
4. Bulb is reset
5. Re-add in app

---

## 9. When to Contact Support

Contact NeuraHome support immediately if:
- Device is completely unresponsive after troubleshooting
- Error persists after factory reset
- Hardware appears damaged
- Safety concerns (lock not securing, electrical issues)
- Warranty claim needed
- Advanced technical assistance required

**Support Channels:**
- **Email:** support@neurahome.com
- **Hotline:** +1-800-NEURA-HOME (24/7)
- **Live Chat:** Available in NeuraHome App
- **Website:** neurahome.com/support

---

## 10. Prevention Tips

### Regular Maintenance
- **Weekly:** Check device status, review activity logs
- **Monthly:** Update firmware, clean sensors, check batteries
- **Quarterly:** Review and optimize automations, remove unused devices

### Best Practices
- Keep firmware updated
- Use quality batteries and power supplies
- Maintain strong WiFi signal
- Regular backups of settings
- Document device configurations

