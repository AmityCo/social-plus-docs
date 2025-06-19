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
                    // Try to refresh token
                    refreshToken();
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