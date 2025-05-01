#!/bin/bash

# Import Bob's public key (optional if already imported)
gpg --import bob_public.asc 2>/dev/null

# Create the message
echo "This is a secret message from Alice to Bob." > original_message.txt

# Encrypt and sign using Bob's public key and Alice's private key
gpg --encrypt --sign --armor \
--recipient bob@example.com \
--local-user alice@example.com \
--output signed_message.asc \
original_message.txt

# Check if file was created
if [[ -f signed_message.asc ]]; then
	echo "✅ Message signed and encrypted successfully as 'signed_message.asc'"
	else
		echo "❌ Error: signed_message.asc was not created. Check for GPG issues."
		fi
		
