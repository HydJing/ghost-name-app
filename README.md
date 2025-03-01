# Ghost Name App

A web application hosted on Google App Engine that generates unique ghost names for users based on their first and last names. Users must log in via Google OAuth, and the app ensures consistent ghost names for returning users while preventing duplicates.

## Project Overview

- **App URL**: 
- **Platform**: Google App Engine (Standard Environment, Free Tier)
- **Language**: Python 3.9
- **Framework**: Flask
- **Database**: Firestore in Datastore mode (via `google.cloud.ndb`)
- **Authentication**: Google OAuth 2.0

### Features
1. **Overview Page**:
   - Lists all taken ghost names with associated emails and user-entered names.
   - Links to "Get a Phantom Name" (or "Change your current Phantom Name" for returning users).
2. **Ghost Name Form**:
   - Requires Google login.
   - Collects user's first and last names.
3. **Ghost Name Results**:
   - Presents 3 unique ghost name options in the format `[First Name] "[Ghost Name]" [Last Name]`.
   - Allows selection and saves to Datastore.

### Technical Requirements
- Hosted on Google App Engine free tier.
- Built with Python 3.9, Flask, and `google.cloud.ndb`.
- Uses HTML/CSS/JS for the frontend.
- Follows Google Python Style Guidelines.

## Setup Instructions

### Prerequisites
- **Google Cloud SDK**: Installed and authenticated (`gcloud init`).
- **Python 3.9**: Installed and added to PATH.
- **Git**: Installed for version control.

## Limitations
- Free tier quotas limit instance hours and storage.
- Static ghost name list restricts scalability.
- No logout functionality.

## Future Improvements
- Dynamic ghost name generation.
- Pagination for the overview page.
- Add logout feature.