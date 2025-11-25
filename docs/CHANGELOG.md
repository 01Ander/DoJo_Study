# DoJo Version Log

## [2.0.0] - 2025-11-25

### Added
- **Core/Campaign Separation**: Established a clear distinction between the DoJo framework (Core) and specific learning paths (Campaigns).
- **Branch Strategy**:
    - `main`: Contains only the stable core system (structure, protocols, templates).
    - `campaign/*`: Dedicated branches for specific subjects (e.g., `campaign/python`).
- **Git Configuration**: Added `.gitignore` to exclude local configuration files (e.g., Obsidian).

### Changed
- Moved all Python-specific content to `campaign/python` branch.
- Cleaned `main` branch to serve as a generic starting point for any student.

### Fixed
- Removed local `.obsidian` configuration from version control.
