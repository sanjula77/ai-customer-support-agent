# NH-Lock Secure+ — User Management Guide
**NeuraHome Systems**

---

## 1. Overview
The NH-Lock Secure+ supports comprehensive user management through the NeuraHome mobile app. You can add permanent users, manage permissions, set up fingerprints, and configure access schedules.

---

## 2. User Types & Permissions

### Admin User
- **Full access** to all lock functions
- Can add/remove users
- Can modify settings
- Can view all activity logs
- Can manage guest access
- **First user** who pairs the lock becomes the admin

### Standard User
- Can unlock/lock the door
- Can view their own activity logs
- Cannot modify settings
- Cannot add/remove other users
- Can be assigned specific access schedules

### Guest User
- Temporary access with PIN only
- Time-limited or one-time use
- Cannot use fingerprint
- Cannot view activity logs
- Automatically expires based on settings

---

## 3. Adding a New Permanent User

### Method 1: Add User via App (Recommended)
1. Open **NeuraHome App**
2. Navigate to **Devices → NH-Lock Secure+**
3. Tap **User Management** or **Users**
4. Tap **+ Add User** or **Add New User**
5. Enter user details:
   - **Name** (e.g., "John Smith", "Family Member")
   - **Email** (optional, for notifications)
   - **Phone number** (optional)
6. Choose authentication method:
   - **PIN Code** (4-8 digits)
   - **Fingerprint** (requires physical access)
   - **Both PIN and Fingerprint**
7. Tap **Save** or **Create User**

### Method 2: Add User with Fingerprint
1. Follow steps 1-5 from Method 1
2. Select **Fingerprint** or **Both**
3. Tap **Start Fingerprint Enrollment**
4. Have the new user place their finger on the sensor
5. Lift and place finger again (repeat 3-5 times)
6. App will confirm when fingerprint is registered
7. Tap **Complete** to finish

### Method 3: Quick Add via Keypad
1. Admin user enters their PIN on the lock keypad
2. Press and hold `*` for 5 seconds
3. Keypad will flash **yellow** (admin mode)
4. Enter `#` + `1` (add user mode)
5. New user enters their desired PIN (4-8 digits)
6. Press `#` to confirm
7. Lock will flash **green** when user is added

---

## 4. Adding Fingerprints to Existing Users

### Steps
1. App → **Devices → NH-Lock Secure+ → User Management**
2. Select the user you want to add fingerprint to
3. Tap **Add Fingerprint** or **Enroll Fingerprint**
4. Have the user place their finger on the lock's fingerprint sensor
5. Lift and place finger again (repeat 3-5 times for better accuracy)
6. App will show progress: "Enrolling... 1/5", "2/5", etc.
7. When complete, app shows "Fingerprint enrolled successfully"
8. You can add up to **3 fingerprints per user** for different fingers

### Tips for Better Fingerprint Recognition
- Clean the sensor before enrollment
- Use dry, clean fingers
- Enroll the same finger multiple times from different angles
- Enroll both index fingers for convenience
- Re-enroll if fingerprint recognition becomes unreliable

---

## 5. Removing Users

### Remove User via App
1. App → **Devices → NH-Lock Secure+ → User Management**
2. Find the user you want to remove
3. Tap the user's name or settings icon
4. Scroll down and tap **Remove User** or **Delete User**
5. Confirm removal (this action cannot be undone)
6. User's PIN and fingerprints will be deleted immediately

### Remove User via Keypad (Admin Only)
1. Admin enters their PIN on keypad
2. Press and hold `*` for 5 seconds (admin mode)
3. Enter `#` + `2` (remove user mode)
4. Enter the user's PIN to remove
5. Press `#` to confirm
6. Lock flashes **red** then **green** when removed

### Bulk Remove Users
1. App → **User Management**
2. Tap **Select** or **Edit Mode**
3. Select multiple users
4. Tap **Delete** or **Remove Selected**
5. Confirm deletion

---

## 6. Editing User Information

### Change User Name
1. App → **User Management → Select User**
2. Tap **Edit** or user name
3. Modify the name
4. Tap **Save**

### Change User PIN
1. App → **User Management → Select User**
2. Tap **Change PIN** or **Security Settings**
3. Enter new PIN (4-8 digits)
4. Confirm new PIN
5. Tap **Save**

### Remove Fingerprint
1. App → **User Management → Select User**
2. Tap **Fingerprints** or **Biometric Settings**
3. Select the fingerprint to remove
4. Tap **Delete** or **Remove**
5. Confirm deletion

---

## 7. User Permissions & Access Control

### Set Access Schedule
1. App → **User Management → Select User**
2. Tap **Access Schedule** or **Time Restrictions**
3. Choose schedule type:
   - **Always** (24/7 access)
   - **Weekdays Only** (Monday-Friday)
   - **Weekends Only** (Saturday-Sunday)
   - **Custom Schedule** (set specific days and times)
4. For custom schedule:
   - Select days of week
   - Set start time and end time
   - Tap **Save**
5. User can only unlock during scheduled times

### Restrict Unlock Methods
1. App → **User Management → Select User**
2. Tap **Unlock Methods** or **Access Methods**
3. Enable/disable:
   - **PIN Code**
   - **Fingerprint**
   - **App Remote Unlock**
4. Save changes

### View-Only Access
1. App → **User Management → Select User**
2. Enable **View Logs Only**
3. User can see activity logs but cannot unlock door

---

## 8. Guest Access Management

### Create Guest PIN
1. App → **Devices → NH-Lock Secure+ → Guest Access**
2. Tap **+ Add Guest PIN**
3. Enter guest name (optional)
4. Set PIN (4-8 digits)
5. Choose access type:
   - **One-time use** (expires after first unlock)
   - **Time-limited** (set expiration date/time)
   - **Recurring** (e.g., every Monday 9 AM - 5 PM)
6. Set number of uses (if applicable)
7. Tap **Create** or **Save**

### Share Guest PIN
1. App → **Guest Access → Select Guest PIN**
2. Tap **Share** or **Send PIN**
3. Choose method:
   - **SMS/Text Message**
   - **Email**
   - **WhatsApp**
   - **Copy to Clipboard**
4. Guest receives PIN with instructions

### Revoke Guest Access
1. App → **Guest Access**
2. Find the guest PIN
3. Tap **Revoke** or **Delete**
4. PIN is immediately deactivated

### View Guest Activity
1. App → **Guest Access → Select Guest PIN**
2. Tap **Activity Log** or **Usage History**
3. View unlock attempts, timestamps, and success/failure

---

## 9. User Activity Logs

### View All Activity
1. App → **Devices → NH-Lock Secure+ → Activity Logs**
2. View list of all unlock/lock events
3. Filter by:
   - **User** (select specific user)
   - **Date Range** (last 7 days, 30 days, 90 days)
   - **Unlock Method** (PIN, fingerprint, app, key)
   - **Status** (successful, failed)

### Activity Log Details
Each log entry shows:
- **Timestamp** (date and time)
- **User Name** (who unlocked)
- **Unlock Method** (PIN, fingerprint, app, physical key)
- **Status** (Success/Failed)
- **Location** (if multiple locks)

### Export Activity Logs
1. App → **Activity Logs**
2. Tap **Export** or **Share**
3. Choose format: **PDF** or **CSV**
4. Select date range
5. Export to email or cloud storage

---

## 10. Advanced User Settings

### Maximum Failed Attempts
1. App → **Devices → NH-Lock Secure+ → Security Settings**
2. Set **Max Failed Attempts** (default: 5)
3. After limit reached, lock enters **lockdown mode** for 60 seconds
4. Admin can adjust this value (3-10 attempts)

### Auto-Lock Delay
1. App → **Devices → NH-Lock Secure+ → Settings**
2. Set **Auto-Lock Delay** (5-30 seconds)
3. Door automatically locks after delay
4. Can be disabled for manual locking only

### Silent Mode
1. App → **User Management → Select User**
2. Enable **Silent Mode**
3. Lock operates without beeps or LED flashes
4. Useful for night-time use

### Notification Settings
1. App → **User Management → Select User**
2. Tap **Notifications**
3. Enable/disable:
   - **Unlock Notifications** (get notified when user unlocks)
   - **Failed Attempt Alerts**
   - **Low Battery Warnings**
   - **Activity Summary** (daily/weekly)

---

## 11. Troubleshooting User Management

### User Cannot Be Added
**Possible Causes:**
- Maximum users reached (lock supports up to 50 users)
- Admin PIN incorrect
- Bluetooth connection lost
- Lock battery too low

**Solutions:**
1. Remove unused users to free up space
2. Verify admin PIN is correct
3. Move phone closer to lock (< 1 meter)
4. Replace lock batteries
5. Restart the app and retry

### Fingerprint Not Enrolling
**Possible Causes:**
- Sensor dirty or damaged
- Finger too wet or dry
- Too many fingerprints already enrolled (max 100 total)

**Solutions:**
1. Clean fingerprint sensor with soft cloth
2. Dry hands completely before enrollment
3. Remove old unused fingerprints
4. Try different finger (index finger works best)
5. Ensure good lighting during enrollment

### User PIN Not Working
**Possible Causes:**
- PIN was changed or removed
- User access schedule restricts access
- Lock in lockdown mode (too many failed attempts)

**Solutions:**
1. Verify PIN in app user management
2. Check user's access schedule
3. Wait for lockdown period to expire (60 seconds)
4. Admin can reset user PIN in app
5. Use physical key as backup

### User Cannot See Activity Logs
**Possible Causes:**
- User doesn't have permission to view logs
- Logs older than 90 days (automatically deleted)
- App not synced with cloud

**Solutions:**
1. Admin must grant "View Logs" permission
2. Activity logs only kept for 90 days
3. Refresh app or check internet connection
4. Admin can export and share logs

---

## 12. Best Practices

### Security Recommendations
- **Change default admin PIN** immediately after setup
- **Use strong PINs** (6-8 digits, avoid common patterns like 1234)
- **Regularly review** user list and remove unused users
- **Enable notifications** for all unlock events
- **Set access schedules** for users who don't need 24/7 access
- **Use fingerprints** for primary users (more secure than PINs)
- **Regularly update firmware** for security patches

### User Management Tips
- **Name users clearly** (e.g., "John - Main User", "Guest - Weekend")
- **Add multiple fingerprints** per user for reliability
- **Test user access** after adding to ensure it works
- **Document guest PINs** and expiration dates
- **Review activity logs weekly** for suspicious activity
- **Remove users immediately** when they no longer need access

---

## 13. Support
For additional help with user management:
- **Email:** support@neurahome.com
- **Hotline:** +1-800-NEURA-HOME
- **Live Chat:** Available in NeuraHome App
- **Website:** neurahome.com/support/lock-users

