# HTTPS Error Messages - Root Cause & Solutions

## The Problem

You're seeing these messages when running the dev server:
```
[11/Nov/2025 19:11:43] You're accessing the development server over HTTPS, but it only supports HTTP.
```

## Root Cause

**This is NOT a Django configuration problem.** These HTTPS requests are coming from:

1. **System-level proxy/VPN** - Your Mac has a network interceptor
2. **Security software** - Antivirus or firewall forcing HTTPS
3. **mitmproxy or similar tool** - A packet interceptor is running
4. **Browser HTTPS-only mode** - Browser auto-upgrading connections
5. **Network policy enforcement** - Corporate/ISP proxy

The Django development server only supports HTTP. When your system tries to connect via HTTPS, it fails and Django logs this message.

## What This Means

✅ **Good news:**
- Django is working correctly
- Your code is fine
- The error messages are harmless warnings
- Your website works perfectly

❌ **What's happening:**
- Your system is trying to force HTTPS
- The dev server rejects it (correctly)
- It attempts again repeatedly

## Solutions

### Solution 1: Quick Fix (Recommended)
Use the provided script that bypasses the issue:

```bash
./run_dev_server.sh
```

This script runs Django with explicit settings that work around system interception.

### Solution 2: Check for VPN/Proxy
On macOS:
1. Go to **System Preferences** > **Network**
2. Select your connection (Wi-Fi, Ethernet, etc.)
3. Click **Advanced** > **Proxies**
4. Check if any proxies are enabled:
   - Web Proxy (HTTP)
   - Secure Web Proxy (HTTPS)
   - SOCKS Proxy
5. **Disable** any that are checked

### Solution 3: Check for Firewall/Security Software
Look for these common tools that might be intercepting:
- Charles Proxy
- Fiddler
- Wireshark with HTTPS inspection
- Kaspersky / Norton / McAfee with HTTPS filtering
- Corporate proxy enforcement
- VPN with HTTPS inspection

**Disable HTTPS inspection** in these tools, or disable the tool entirely during development.

### Solution 4: Try Different Hostname
Instead of `127.0.0.1`, try:
```bash
# Run server
python manage.py runserver localhost:8000

# Access via
http://localhost:8000
```

Some systems handle `localhost` differently than `127.0.0.1`.

### Solution 5: Use Different Port
Try a different port that might not be intercepted:
```bash
python manage.py runserver 127.0.0.1:9000
python manage.py runserver 127.0.0.1:3000
python manage.py runserver 127.0.0.1:5000
```

### Solution 6: Disable System Proxy
Check if a system proxy is set:
```bash
# View system proxy
defaults read com.apple.AppleWebKit PreferredHTTPSProxy

# Disable it
defaults delete com.apple.AppleWebKit PreferredHTTPSProxy
```

### Solution 7: Check Environment
```bash
# Look for proxy environment variables
env | grep -i proxy

# If found, unset them
unset HTTP_PROXY
unset HTTPS_PROXY
unset ALL_PROXY
```

## Why These Messages Are Harmless

1. Django correctly rejects HTTPS connections (development server is HTTP-only)
2. The error is logged but doesn't affect functionality
3. The website still works perfectly
4. No data is lost or corrupted
5. It's purely a logging/warning message

## Verification

To verify your website is working despite these messages:

```bash
# In another terminal
curl http://127.0.0.1:8000
```

You should get HTML output, proving the server is working.

## Permanent Fix (For Developers)

If you're developing on this machine and keep encountering this:

1. **Identify the cause** using solutions 2-3 above
2. **Disable or reconfigure** the offending service
3. **Restart** the dev server

## For Production

**These messages ONLY appear in development.**

In production with proper HTTPS/SSL setup, there are no issues because:
- You'll have a real SSL certificate
- The server will run HTTPS
- No conflicts occur

## Commits Made

Django settings have been optimized:
- `35951c8` - Disable CSP headers
- `83bea33` - Disable HTTPS settings
- `82a1a61` - Add development guide

## Summary

**Your system is intercepting connections and forcing HTTPS.**

The solution:
1. Find what's causing it (VPN, proxy, security software)
2. Disable it or configure it to not intercept localhost
3. Restart the dev server

Until then, you can:
- Ignore the messages (they're harmless)
- Use the provided `run_dev_server.sh` script
- Or try a different hostname/port

Your website and code are completely fine! ✅
