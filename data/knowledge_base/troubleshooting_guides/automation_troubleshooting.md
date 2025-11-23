# Automation Troubleshooting Guide
**NeuraHome Systems**

---

## 1. Overview
This guide helps troubleshoot automation issues, including rules not triggering, conflicting automations, and performance problems.

---

## 2. Automation Not Triggering

### Rule Not Executing
**Symptoms:**
- Automation created but never runs
- Trigger conditions met but no action
- No errors shown

**Solutions:**
1. **Verify Automation Enabled:**
   - App → Automation → Select Rule
   - Ensure "Enabled" toggle is ON
   - Check if paused or disabled

2. **Check Trigger Conditions:**
   - Review all trigger conditions
   - Ensure ALL conditions are met (if using AND logic)
   - Test trigger manually

3. **Verify Device Status:**
   - Ensure trigger device is online
   - Check device is responding
   - Test device control manually

4. **Check Automation Logs:**
   - App → Automation → Logs
   - See if automation attempted to run
   - Check for error messages

### Automation Runs But Action Fails
**Symptoms:**
- Automation triggers correctly
- Action device doesn't respond
- Partial execution

**Solutions:**
1. **Check Action Device:**
   - Verify device is online
   - Test device control manually
   - Check device battery/power

2. **Review Action Settings:**
   - Verify action is configured correctly
   - Check device name matches
   - Ensure action is valid

3. **Check Device Limits:**
   - Some devices have rate limits
   - Too many commands may be ignored
   - Add delays between actions

### Delayed Automation Execution
**Symptoms:**
- Automation runs but with delay
- Slow response times
- Not executing immediately

**Solutions:**
1. **Check Hub Performance:**
   - Hub Settings → Performance
   - If CPU/Memory high, reduce automations
   - Restart hub if needed

2. **Network Issues:**
   - Check WiFi signal strength
   - Verify devices are online
   - Reduce network congestion

3. **Automation Priority:**
   - Check automation priority settings
   - Lower priority automations may be delayed
   - Increase priority if needed

---

## 3. Conflicting Automations

### Multiple Automations Interfering
**Symptoms:**
- Devices turn on/off unexpectedly
- Conflicting actions
- Unpredictable behavior

**Solutions:**
1. **Review All Automations:**
   - List all automations affecting same device
   - Identify conflicts
   - Disable or modify conflicting rules

2. **Use Conditions:**
   - Add conditions to prevent conflicts
   - Example: "Only if device is off" before turning on
   - Use time-based conditions

3. **Set Priorities:**
   - Assign priorities to automations
   - Higher priority runs first
   - Resolve conflicts in favor of priority

### Automation Loops
**Symptoms:**
- Device turns on/off repeatedly
- Continuous cycling
- Automation triggers itself

**Solutions:**
1. **Break the Loop:**
   - Add condition to prevent re-triggering
   - Example: "Only if device was off for 5 minutes"
   - Use cooldown periods

2. **Review Triggers:**
   - Ensure action doesn't trigger same automation
   - Check for circular dependencies
   - Modify trigger conditions

3. **Disable Temporarily:**
   - Disable automation to stop loop
   - Review and fix logic
   - Re-enable after fixing

---

## 4. Advanced Automation Issues

### Geofencing Not Working
**Symptoms:**
- Auto-unlock when arriving doesn't work
- Location-based automations fail
- Geofence not detected

**Solutions:**
1. **Check Location Permissions:**
   - Phone Settings → Apps → NeuraHome → Permissions
   - Enable "Location - Always"
   - Grant background location access

2. **Verify Geofence Settings:**
   - App → Automation → Geofencing
   - Check radius is appropriate (50-500 meters)
   - Ensure correct location set

3. **Phone Settings:**
   - Disable battery optimization for app
   - Allow background app refresh
   - Keep app running in background

### Time-Based Automations Off Schedule
**Symptoms:**
- Automations run at wrong time
- Time zone issues
- Sunrise/sunset times incorrect

**Solutions:**
1. **Check Time Zone:**
   - App → Settings → Time Zone
   - Verify correct time zone set
   - Update if changed location

2. **Verify Schedule:**
   - Review automation schedule
   - Check AM/PM settings
   - Verify days of week

3. **Sunrise/Sunset:**
   - App uses device location for sun times
   - Verify location is correct
   - Manually adjust if needed

---

## 5. Performance Optimization

### Too Many Automations
**Symptoms:**
- Hub slow to respond
- Automations delayed
- System performance issues

**Solutions:**
1. **Reduce Automation Count:**
   - Combine similar automations
   - Remove unused automations
   - Optimize existing rules

2. **Simplify Logic:**
   - Reduce complex conditions
   - Use simpler triggers
   - Avoid nested conditions

3. **Use Scenes:**
   - Replace multiple automations with scenes
   - Scenes execute faster
   - Easier to manage

### Automation Best Practices
1. **Group Related Actions:**
   - Use scenes for multiple device control
   - Reduces automation count
   - Faster execution

2. **Use Delays Wisely:**
   - Add delays only when necessary
   - Too many delays slow system
   - Keep delays short (< 30 seconds)

3. **Test Automations:**
   - Test after creating
   - Verify all conditions work
   - Monitor for first few days

---

## 6. Support
For automation help:
- **Email:** support@neurahome.com
- **Hotline:** +1-800-NEURA-HOME

