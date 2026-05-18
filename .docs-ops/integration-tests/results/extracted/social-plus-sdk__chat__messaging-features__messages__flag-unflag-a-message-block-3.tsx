/// <reference path="../../preamble.d.ts" />
// source: social-plus-sdk/chat/messaging-features/messages/flag-unflag-a-message.mdx:1360-1375

    // Example flag confirmation dialog
    function showFlagConfirmation(messageId, reason) {
        return new Promise((resolve) => {
            const modal = document.createElement('div');
            modal.innerHTML = `
                <div class="flag-confirmation-modal">
                    <h3>Flag this message?</h3>
                    <p>Reason: ${reason}</p>
                    <p>This will report the message to moderators for review.</p>
                    <button onclick="resolve(true)">Confirm</button>
                    <button onclick="resolve(false)">Cancel</button>
                </div>
            `;
            document.body.appendChild(modal);
        });
    }
