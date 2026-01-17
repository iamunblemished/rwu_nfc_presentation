from django.db import models

class Keycard(models.Model):
    uid = models.CharField(max_length=100, unique=True, help_text="The unique ID of the NFC tag")
    owner_name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.owner_name} ({self.uid})"

class AccessLog(models.Model):
    # We store the UID even if the card isn't in our database (for security auditing)
    scanned_uid = models.CharField(max_length=100)
    granted = models.BooleanField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        status = "ALLOWED" if self.granted else "DENIED"
        return f"{self.timestamp.strftime('%Y-%m-%d %H:%M')} - {status}: {self.scanned_uid}"
