# GymFlow Pro - Learning Notes

## Day 1 - Done ✅
- Created project folder with backend/ and frontend/
- Installed Python, Node.js, VS Code, Git
- Initialized Git repo
- Created Python virtual environment

## Questions I have:
- (write anything you're confused about here)

Day 3

TABLES WE NEED:
===============

1. GymProfile      → the gym itself (name, address, owner)
2. Plan            → membership plans (Basic, Standard, Premium)
3. Member          → gym members (name, phone, which plan)
4. Payment         → fee payment records (who paid, how much, when)
5. SMSLog          → track every SMS sent (to who, what, when)

RELATIONSHIPS:
==============
GymProfile  →  one owner (Django's built-in User)
Plan        →  belongs to one GymProfile
Member      →  belongs to one GymProfile
Member      →  belongs to one Plan
Payment     →  belongs to one Member
SMSLog      →  belongs to one Member