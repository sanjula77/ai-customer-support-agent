# Network Connectivity Issues — Comprehensive Troubleshooting
**NeuraHome Systems**

---

## 1. Overview
Network connectivity issues can affect all NeuraHome devices. This guide covers WiFi, Ethernet, Zigbee, and Bluetooth connectivity problems.

---

## 2. WiFi Connectivity Issues

### Device Cannot Connect to WiFi
**Symptoms:**
- Device shows "WiFi Connection Failed"
- Cannot complete setup
- Device offline after working

**Solutions:**
1. **Verify WiFi Requirements:**
   - Most devices require **2.4 GHz WiFi** (not 5 GHz)
   - Check router has 2.4 GHz enabled
   - Some devices support both (Hub X1)

2. **Check WiFi Password:**
   - Ensure password is correct
   - No special characters causing issues
   - Try re-entering password

3. **Signal Strength:**
   - Move device closer to router
   - Check signal strength (should be > -70 dBm)
   - Remove physical obstructions

4. **Router Settings:**
   - Disable MAC filtering temporarily
   - Check device limit on router
   - Ensure router not blocking device

### WiFi Keeps Disconnecting
**Symptoms:**
- Device connects then disconnects
- Intermittent connectivity
- Works sometimes, not others

**Solutions:**
1. **Router Channel Interference:**
   - Change router WiFi channel
   - Use WiFi analyzer to find best channel
   - Avoid crowded channels (1, 6, 11)

2. **Power Saving Mode:**
   - Disable WiFi power saving on router
   - Some routers disconnect idle devices
   - Check router settings

3. **DHCP Lease Time:**
   - Increase DHCP lease time
   - Set to 24 hours or longer
   - Prevents IP address conflicts

4. **Router Firmware:**
   - Update router firmware
   - Old firmware may have bugs
   - Check router manufacturer website

### Slow WiFi Performance
**Symptoms:**
- Commands take long to execute
- Delayed responses
- Timeouts

**Solutions:**
1. **Reduce Network Load:**
   - Disconnect unused devices
   - Limit bandwidth-heavy activities
   - Prioritize smart home traffic

2. **Upgrade Router:**
   - Older routers may be slow
   - Consider WiFi 6 router
   - Better handling of many devices

3. **Mesh Network:**
   - Add WiFi extenders or mesh nodes
   - Improves coverage and speed
   - Reduces dead zones

---

## 3. Zigbee Network Issues

### Zigbee Devices Not Pairing
**Symptoms:**
- Device not discovered by hub
- Pairing fails
- "Device Not Found" errors

**Solutions:**
1. **Check Hub Zigbee Status:**
   - Hub Settings → Zigbee → Status
   - Ensure Zigbee coordinator active
   - Restart hub if needed

2. **Distance and Obstacles:**
   - Move device closer to hub
   - Zigbee range: ~30-50 meters indoors
   - Reduce obstacles (walls, metal)

3. **Zigbee Channel:**
   - Change Zigbee channel if interference
   - Avoid WiFi channels (1, 6, 11)
   - Use channels 15, 20, or 25

4. **Device-Specific:**
   - Follow device pairing instructions exactly
   - Some devices have specific pairing modes
   - Check device manual

### Zigbee Devices Disconnect Randomly
**Symptoms:**
- Devices work then go offline
- Intermittent connectivity
- Range issues

**Solutions:**
1. **Add Zigbee Repeater:**
   - Install Zigbee smart plug
   - Acts as signal repeater
   - Extends network range

2. **Reduce Interference:**
   - Move hub away from WiFi router
   - Avoid 2.4 GHz devices nearby
   - Use 5 GHz WiFi if possible

3. **Network Topology:**
   - Ensure mesh network formed
   - Devices should route through each other
   - Check network map in app

4. **Power Issues:**
   - Battery devices may disconnect if low
   - Check battery levels
   - Replace batteries

---

## 4. Bluetooth Connectivity Issues

### Bluetooth Pairing Fails
**Symptoms:**
- Device not discovered
- Pairing timeout
- "Bluetooth Error" messages

**Solutions:**
1. **Phone Settings:**
   - Enable Bluetooth and Location
   - Some phones require location for BLE
   - Grant app permissions

2. **Distance:**
   - Move phone within 1 meter of device
   - Bluetooth range is limited
   - Remove obstacles

3. **Interference:**
   - Turn off other Bluetooth devices
   - Reduce WiFi interference
   - Try different location

4. **App Permissions:**
   - Check app has Bluetooth permission
   - Re-grant if needed
   - Restart app

### Bluetooth Connection Drops
**Symptoms:**
- Connection works then drops
- Unstable connection
- Reconnection required

**Solutions:**
1. **Phone Bluetooth:**
   - Restart phone Bluetooth
   - Clear Bluetooth cache
   - Update phone OS

2. **Device Battery:**
   - Low battery affects Bluetooth
   - Replace batteries
   - Check power supply

3. **Interference:**
   - Move away from WiFi router
   - Reduce other 2.4 GHz devices
   - Use 5 GHz WiFi

---

## 5. Ethernet Connectivity Issues

### Ethernet Not Working
**Symptoms:**
- Hub shows "Ethernet Disconnected"
- No network via Ethernet
- Falls back to WiFi

**Solutions:**
1. **Cable Check:**
   - Test cable with another device
   - Ensure cable not damaged
   - Try different cable

2. **Port Check:**
   - Try different router port
   - Check port not disabled
   - Verify port working

3. **Hub Settings:**
   - Hub Settings → Network → Ethernet
   - Enable Ethernet priority
   - Check Ethernet status

4. **Router Configuration:**
   - Check router port settings
   - Ensure port not blocked
   - Verify router firmware

---

## 6. Network-Wide Issues

### All Devices Offline
**Symptoms:**
- Multiple devices offline
- Hub still online
- Network appears fine

**Solutions:**
1. **Check Internet:**
   - Test internet connection
   - Check ISP status
   - Verify router internet

2. **Router Restart:**
   - Restart router
   - Wait 5 minutes
   - Devices should reconnect

3. **Cloud Service:**
   - Check neurahome.com/status
   - Service may be down
   - Wait for resolution

### Slow Response Times
**Symptoms:**
- Commands take long
- Delayed execution
- Timeouts

**Solutions:**
1. **Network Load:**
   - Reduce network traffic
   - Limit bandwidth usage
   - Prioritize smart home

2. **Router Performance:**
   - Check router CPU usage
   - Too many devices may overload
   - Consider router upgrade

3. **Local Processing:**
   - Enable local processing on hub
   - Reduces cloud dependency
   - Faster response

---

## 7. Advanced Network Troubleshooting

### Port Forwarding Issues
**Symptoms:**
- Remote access doesn't work
- Port forwarding configured but fails
- External access blocked

**Solutions:**
1. **Verify Ports:**
   - Required ports: 443 (HTTPS), 8883 (MQTT)
   - Check firewall allows ports
   - Verify port forwarding rules

2. **Dynamic DNS:**
   - Use dynamic DNS service
   - Updates IP automatically
   - Easier than static IP

3. **VPN Alternative:**
   - Use VPN for remote access
   - More secure than port forwarding
   - Works behind firewalls

### Network Segmentation
**Symptoms:**
- Devices on different networks can't communicate
- VLAN isolation issues
- Guest network problems

**Solutions:**
1. **Network Configuration:**
   - Ensure devices on same network
   - Check VLAN settings
   - Allow inter-device communication

2. **Guest Network:**
   - Most devices need main network
   - Guest networks often isolated
   - Move devices to main network

3. **Firewall Rules:**
   - Allow device-to-device communication
   - Check firewall rules
   - May need router configuration

---

## 8. Support
For network issues:
- **Email:** support@neurahome.com
- **Hotline:** +1-800-NEURA-HOME
- **Network Support:** Available for complex setups

