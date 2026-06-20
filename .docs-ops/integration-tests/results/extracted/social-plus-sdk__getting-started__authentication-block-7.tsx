/// <reference path="../../preamble.d.ts" />
// source: social-plus-sdk/getting-started/authentication.mdx:453-489

    // Listen to session state changes
    import { Client } from '@amityco/ts-sdk';
    import React, { FC, useEffect, useState } from 'react';
    
    const SessionState: FC = () => {
        const [sessionState, setSessionState] = useState('');
        useEffect(() => {
            return Client.onSessionStateChange((state: Amity.SessionStates) => {
                switch (state) {
                    case 'notLoggedIn':
                        // Show login form
                        showLoginForm();
                        break;
                    case 'establishing':
                        // Show loading spinner
                        showLoadingSpinner();
                        break;
                    case 'established':
                        // Hide spinner, navigate to app
                        hideLoadingSpinner();
                        navigateToApp();
                        break;
                    case 'tokenExpired':
                        // Attempt to refresh token (Optional)
                         showTokenRefreshIndicator()
                        break;
                    case 'terminated':
                        // Handle termination
                        handleSessionTermination();
                        break;
                }
            }
            );
        }, []);
    
      return null;
    };
