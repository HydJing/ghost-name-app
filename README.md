# Ghost Name App Design Document

## Overview
The Ghost Name App is a web application deployed on Google App Engine that allows users to authenticate via Google OAuth, enter their first and last names, and select a unique phantom name from a predefined list.

The app displays an overview of taken ghost names with user details, fulfilling the technical exercise requirements.

This document outlines the solution’s design, technology stack, current limitations, and potential future enhancements.

## Solution Design

### Architecture
- **Framework**: Flask, a lightweight Python web framework, drives the application’s routing and templating.
- **Deployment**: Hosted on Google App Engine Standard Environment (Python 3.9), leveraging its free tier for scalability and serverless operation.
- **Modularity**: The app uses Flask blueprints to separate authentication (`auth`) and phantom name functionality (`phantom`), enhancing maintainability.
- **Data Storage**: Google Cloud Datastore (via NDB) stores ghost names and user assignments persistently.

### Components
1. **Authentication**:
   - **Route**: `/login` and `/callback` (in `routes/auth.py`).
   - **Flow**: Users authenticate via Google OAuth 2.0, redirecting to Google’s authorization page and back to `/callback` for token exchange and session setup.

2. **Overview Page**:
   - **Route**: `/` (in `routes/phantom.py`).
   - **Functionality**: Displays a list of taken ghost names with user details (first name, ghost name, last name, email) fetched from Datastore.

3. **Phantom Name Form**:
   - **Route**: `/phantom-form` (in `routes/phantom.py`).
   - **Functionality**: Accepts user input (first/last names) via GET (form display) and POST (submission), storing names in the session.

4. **Phantom Name Results**:
   - **Route**: `/phantom-results` (in `routes/phantom.py`).
   - **Functionality**: Displays three available ghost name options (GET) and saves the selected name to Datastore (POST).

### Data Models
- **GhostName** (`models.py`):
  - Properties: `name` (string), `description` (string), `is_taken` (boolean, default False).
  - Purpose: Stores the list of available ghost names and their status.
- **UserGhostName** (`models.py`):
  - Properties: `email` (string), `first_name` (string), `last_name` (string), `ghost_name` (string).
  - Purpose: Tracks user-assigned ghost names.

### Workflow
1. User visits `/`, sees taken ghost names, and clicks "Login with Google" if not authenticated.
2. After OAuth, user is redirected to `/`, then clicks "Get a Phantom name" to access `/phantom-form`.
3. User submits names, redirected to `/phantom-results`, selects a ghost name, and saves it, returning to `/`.

## Technology Used

- **Flask (2.3.3)**: Core web framework for routing, templating, and session management.
- **Google App Engine (Python 3.9)**: Serverless hosting platform, free tier used (`runtime: python39` in `app.yaml`).
- **Google Cloud NDB (2.2.0)**: Datastore client for persistent storage of ghost names and user data.
- **Google OAuth 2.0 (google-auth-oauthlib 1.2.0)**: Authentication via Google accounts.
- **Gunicorn (20.1.0)**: WSGI server for running Flask on App Engine.
- **Python Standard Libraries**: `os`, `random`, `logging` for utilities and debugging.
- **HTML/CSS**: Jinja2 templates (`templates/`) and basic styling (`static/style.css`).

## Limitations

1. **Hardcoded OAuth Credentials**:
   - **Issue**: `config.py` uses hardcoded `client_id` and `client_secret` due to persistent GCS deployment issues with Secret Manager integration.
   - **Impact**: Security risk in production; not scalable for team use.

2. **Filesystem-Based Session Storage**:
   - **Issue**: Flask’s default session storage uses the server filesystem, unsuitable for multi-instance scaling on App Engine.
   - **Impact**: Session data may not persist across instances, affecting user experience.

3. **Static Ghost Name List**:
   - **Issue**: Ghost names are loaded from a CSV (`ghost_names.csv`) via a script, not dynamically editable.
   - **Impact**: Limited scalability; adding names requires redeployment or manual Datastore updates.

4. **Free Tier Constraints**:
   - **Issue**: Relies on App Engine’s free tier (28 instance hours/day, 1GB storage).
   - **Impact**: Potential downtime or scaling limits under heavy use.

5. **Deployment Challenges**:
   - **Issue**: Repeated `[7]` GCS errors during `gcloud app deploy`, resolved temporarily with manual permissions.
   - **Impact**: Indicates underlying bucket/service account sync issues.

## Future Improvements

1. **Secret Manager Integration**:
   - **Plan**: Replace hardcoded OAuth credentials with Google Secret Manager fetches in `config.py`.
   - **Benefit**: Enhances security and allows team credential management.

2. **Datastore-Based Sessions**:
   - **Plan**: Implement a custom `NdbSessionInterface` to store sessions in Datastore.
   - **Benefit**: Ensures session persistence across App Engine instances.

3. **Dynamic Ghost Name Management**:
   - **Plan**: Add an admin route (e.g., `/admin/add-name`) to dynamically update ghost names in Datastore.
   - **Benefit**: Removes CSV dependency, improves scalability.

4. **Logout Functionality**:
   - **Plan**: Add a `/logout` route to clear sessions and revoke OAuth tokens.
   - **Benefit**: Enhances user control and security.

5. **Pagination for Overview**:
   - **Plan**: Implement pagination or lazy loading for the taken names list.
   - **Benefit**: Improves performance with many users.

6. **Resolve Deployment Issues**:
   - **Plan**: Investigate GCS staging bucket permissions (e.g., bucket policy, IAM sync) with GCP support.
   - **Benefit**: Ensures reliable deployments without manual fixes.

## Conclusion
The Ghost Name App meets the technical exercise requirements with a functional, modular design hosted on Google App Engine. While it currently relies on temporary workarounds (e.g., hardcoded OAuth), the outlined improvements address these limitations, preparing it for production use. Unit tests (`tests/test_app.py`) validate core functionality, enhancing reliability.

Author: [Your Full Name]  
Date: March 3, 2025