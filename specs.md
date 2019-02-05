
# Caiwan's note taking app - v0.1.alpha

'NOTES' is a self-manager note-taking system that is designed to follow the GTD method. This document roughly lists all the features, that are meant to be tested mainly on server the side.

## User management

This version focuses only on single-user usage, and does not contain any collaborative features.
However in later version there will be a collaborative version added to support small teams. See limitations below.

- A user can log in.
- A user can see it's notes, tasks, milestones, and all the metadata attached to them like tags, and categories where their stuff belongs to.
- A user can change it's settings.
- Settings are in key-value flavor.
- There's a document containing all the available keys for settings.
- Primarily used by 3rd party sync features to store and edit api keys.
- A user can change their password
- Password is encrypted with BCrypt

**Limitations** that will be changed in future version:

- There's no register function (will be added later on)
- Only a global admin user can manage users
- There's no email notification for registering, and changing password
- There's no 3rd party SSO login feature like Google, Facebook, etc.
- A user can't has any additional roles than their default ones

### Admin features

- It's an internal role of `ADMIN`
- Add user
- Remove user
- Activate/deactivate user
- Assign roles to them

## Notes

- A user can add, edit and remove a note
- One created note is owned by the user that crated it
- A note can have multiple tags
- Tags assigned to the notes can be changed
- A note can belong to a single category
- A note can has an expiration / due date
- A note can have tasks attached to it
- Attached tasks inherits the notes due date, unless it was not set individually
- A note can have attachments form 3rd party external cloud storage app.
- A note can be pinned and unpinned
- Pinned notes are appear on the top of the page
- A note can be archived and unarchived
- Archived notes are appear on the bottom of the page
- Other notes are appear in between.
- A note can be deleted after confirmation

## Attachments

- A user can add and delete attachments to a note
- It can be selected from a 3rd party cloud
- A provider id is stored (in which service is the file is located at)
- An external id is stored (to locate / open it via clicking on it)
- A filename is being stored (to display it on the page)

**Limitations:**

- Only Google drive is supported, but it's open to support any other app like Dropbox, OneDrive or Apple Cloud (or whatever)
- Upon deletion of an external file the local link will not be deleted - This will not fixed either

## Categories

- A user can add / remove / edit categories
- Categories can be nested into a tree structure
- Upon deletion all the document objects (notes, tasks) that are belong to one category will be moved to it's parent
- If a deleted note had no parent, it will be moved to `null`
- A user can filter their documents to categories which being shown
- Optionally it can filter ot one single category or all of it's subtree
- A user can merge two categories together, moving all the documents under another category
- The category that is being merged will be deleted
- Categories can get archived which can be hidden on the sidebar for clear view
- Archived category doesn't necessary archives all the documents in it
- Categories can get "protected", which also can get filtered from view, and all the documents are eager filtered out from all the views
- To filter documents to a "protected category" requires an extra confirmation from the user to prevent accidental clicking on it

## Tags
## Todos / Tasks
## Worklog / Pomodoro

## Fuzzy search
## 3rd party sync options
