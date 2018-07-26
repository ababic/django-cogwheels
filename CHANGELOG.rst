Changelog
=========

0.1.1 (XX.XX.XXXX) (IN DEVELOPMENT)
-----------------------------------

- Default deprecation warning messages have been updated to include an indication of when a deprecated setting will be removed, and better explain the consequences of not updating.
- Default deprecation warning messages no longer include text to indicate that developers should "review the release notes and/or documentation". In cases where further information is required, it should be provided as ``additional_guidance``, which may also include a hyperlink to the relevant release notes / documentation where considered useful.
- ``DeprecatedAppSetting`` now supports an ``additional_guidance`` argument at initialisation, that can be used to add further context-specific information for each deprecation as required, which will be appended to the default warning text.
- Added the ``is_value_from_deprecated_setting()`` method to ``BaseAppSettingsHelper`` to help developers determine where a setting value came from when dealing settings that replace deprecated settings.
- Added support for deprecation scenarios where a new setting might replace multiple other settings.
- Renamed the ``get_raw()`` method on ``BaseAppSettingsHelper`` to ``get()`` .


0.1.0 (27.06.2018)
------------------

- Considered suitable for production


0.0.1 (22.06.2018)
------------------

- Initial commit
