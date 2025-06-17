# Customization Basics

## Configuration file

Our UIKit v4 supports customization in a single place by modifying a `config.json` file in related UIKit repository. This configuration file includes all necessary data to customize the appearance of each pages, components and elements that we allow to do customization.

<details>

<summary>Sample <code>config.json</code> file</summary>

```json
{
  "preferred_theme": "default",
  "theme": {
    "light": {
      "primary_color": "#1054DE",
      "secondary_color": "#292B32",
      "base_color": "#292b32",
      "base_shade1_color": "#636878",
      "base_shade2_color": "#898e9e",
      "base_shade3_color": "#a5a9b5",
      "base_shade4_color": "#ebecef",
      "alert_color": "#FA4D30",
      "background_color": "#FFFFFF",
    },
    "dark": {
      "primary_color": "#1054DE",
      "secondary_color": "#292B32",
      "base_color": "#ebecef",
      "base_shade1_color": "#a5a9b5",
      "base_shade2_color": "#6e7487",
      "base_shade3_color": "#40434e",
      "base_shade4_color": "#292b32",
      "alert_color": "#FA4D30",
      "background_color": "#191919",
    }
  },
  "excludes": [
  ],
  "customizations": {
    "select_target_page/*/*": {
      "page_theme": {
        "light_theme": {
          "primary_color": "#1D1234",
          "secondary_color": "#AB1234"
        }
      },
      "title": "Share to"
    },
    "select_target_page/*/back_button": {
      "back_icon": "back.png"
    },
    "camera_page/*/*": {
      "resolution": "720p",
      "theme": {
        "light": {
          "primary_color": "#1054DE",
          "secondary_color": "#292B32",
          "base_color": "#292b32",
          "base_shade1_color": "#636878",
          "base_shade2_color": "#898e9e",
          "base_shade3_color": "#a5a9b5",
          "base_shade4_color": "#ebecef",
          "alert_color": "#FA4D30",
          "background_color": "#FFFFFF",
        },
        "dark": {
          "primary_color": "#1054DE",
          "secondary_color": "#292B32",
          "base_color": "#ebecef",
          "base_shade1_color": "#a5a9b5",
          "base_shade2_color": "#6e7487",
          "base_shade3_color": "#40434e",
          "base_shade4_color": "#292b32",
          "alert_color": "#FA4D30",
          "background_color": "#191919",
        }
      }
    },
    "camera_page/*/close_button": {
      "close_icon": "close.png",
      "background_color": "#80000000"
    },
    "create_story_page/*/*": {},
    "create_story_page/*/back_button": {
      "back_icon": "back.png",
      "background_color": "#80000000"
    },
    "create_story_page/*/aspect_ratio_button": {
      "aspect_ratio_icon": "aspect_ratio.png",
      "background_color": "#80000000"
    },
    "create_story_page/*/story_hyperlink_button": {
      "hyperlink_button_icon": "hyperlink_button.png",
      "background_color": "#80000000"
    },
    "create_story_page/*/hyper_link": {
      "hyper_link_icon": "hyper_link.png",
      "background_color": "#80000000"
    },
    "create_story_page/*/share_story_button": {
      "share_icon": "share_story_button.png",
      "background_color": "#FFFFFF",
      "hide_avatar": false
    },
    "story_page/*/*": {},
    "story_page/*/progress_bar": {
      "progress_color": "#FFFFFF",
      "background_color": "#50FFFFFF"
    },
    "story_page/*/overflow_menu": {
      "overflow_menu_icon": "threeDot.png"
    },
    "story_page/*/close_button": {
      "close_icon": "close.png"
    },
    "story_page/*/story_impression_button": {
      "impression_icon": "impressionIcon.png"
    },
    "story_page/*/story_comment_button": {
      "comment_icon": "comment.png",
      "background_color": "#1234DD"
    },
    "story_page/*/story_reaction_button": {
      "reaction_icon": "like.png",
      "background_color": "#1243EE"
    },
    "story_page/*/create_new_story_button": {
      "create_new_story_icon": "plus.png",
      "background_color": "#1243EE"
    },
    "story_page/*/speaker_button": {
      "mute_icon": "mute.png",
      "unmute_icon": "unmute.png",
      "background_color": "#1243EE"
    },
    "*/edit_comment_component/*": {
    },
    "*/edit_comment_component/cancel_button": {
      "cancel_icon": "",
      "cancel_button_text": "cancel",
      "background_color": "#1243EE"
    },
    "*/edit_comment_component/save_button": {
      "save_icon": "",
      "save_button_text": "Save",
      "background_color": "#1243EE"
    },
    "*/hyper_link_config_component/*": {
      "theme": {
        "light": {
          "primary_color": "#1054DE",
          "secondary_color": "#292B32",
          "base_color": "#292b32",
          "base_shade1_color": "#636878",
          "base_shade2_color": "#898e9e",
          "base_shade3_color": "#a5a9b5",
          "base_shade4_color": "#ebecef",
          "alert_color": "#FA4D30",
          "background_color": "#FFFFFF",
        },
        "dark": {
          "primary_color": "#1054DE",
          "secondary_color": "#292B32",
          "base_color": "#ebecef",
          "base_shade1_color": "#a5a9b5",
          "base_shade2_color": "#6e7487",
          "base_shade3_color": "#40434e",
          "base_shade4_color": "#292b32",
          "alert_color": "#FA4D30",
          "background_color": "#191919",
        }
      }
    },
    "*/hyper_link_config_component/done_button": {
      "done_icon": "",
      "done_button_text": "Done",
      "background_color": "#1243EE"
    },
    "*/hyper_link_config_component/cancel_button": {
      "cancel_icon": "",
      "cancel_button_text": "Cancel"
    },
    "*/comment_tray_component/*": {
      "theme": {
        "light": {
          "primary_color": "#1054DE",
          "secondary_color": "#292B32",
          "base_color": "#292b32",
          "base_shade1_color": "#636878",
          "base_shade2_color": "#898e9e",
          "base_shade3_color": "#a5a9b5",
          "base_shade4_color": "#ebecef",
          "alert_color": "#FA4D30",
          "background_color": "#FFFFFF",
        },
        "dark": {
          "primary_color": "#1054DE",
          "secondary_color": "#292B32",
          "base_color": "#ebecef",
          "base_shade1_color": "#a5a9b5",
          "base_shade2_color": "#6e7487",
          "base_shade3_color": "#40434e",
          "base_shade4_color": "#292b32",
          "alert_color": "#FA4D30",
          "background_color": "#191919",
        }
      }
    },
    "*/story_tab_component/*": {
    },
    "*/story_tab_component/story_ring": {
      "progress_color": [
        "#339AF9",
        "#78FA58"
      ],
      "background_color": [
        "#EBECEF"
      ]
    },
    "*/story_tab_component/create_new_story_button": {
      "create_new_story_icon": "plus.png",
      "background_color": "#1243EE"
    },
    "*/*/close_button": {
      "close_icon": "close.png"
    }
  }
}
```



</details>

## Global Theme

**Applying a theme to application**

UIKit will support **preferred\_theme** property in configuration.

* `default` respects the device settings.
* `light` forcefully set light theme regardless of device settings.
* `dark` forcefully set dark theme regardless of device settings.

```json
"preferred_theme": "default"
```

**Available color properties in Light and Dark theme**

We support `light` and `dark` theme, you can modify primary, secondary, base and shaded colors, alert and background colors for your app theme.

* `primary` - primary color for the app, used for action button and highlighted text.
* `secondary` - secondary color for the app, used for border and secondary action button.
* `base` - used as primary text color in title, label and body.
* `base_shade1` - used as secondary text color in description, slightly lighter than `base` color in `light` theme and slightly dimmer than `base` color in `dark` theme.
* `base_shade2` - used as tertiary text color in secondary description, inactive and hint text, slightly lighter than `base_shade1` color in `light` theme and slightly dimmer than `base_shade1` color in `dark` theme.
* `base_shade3` - used as disabled text color, slightly lighter than `base_shade2` color in `light` theme and slightly dimmer than `base_shade2` color in `dark` theme.
* `base_shade4` - optional, slightly lighter than `base_shade3` color in `light` theme and slightly dimmer than `base_shade3` color in `dark` theme.
* `alert` - used for error button and text.
* `background` - used for background color of the page or component.

```json
"theme": {
    "light": {
      "primary_color": "#1054DE",
      "secondary_color": "#292B32",
      "base_color": "#292b32",
      "base_shade1_color": "#636878",
      "base_shade2_color": "#898e9e",
      "base_shade3_color": "#a5a9b5",
      "base_shade4_color": "#ebecef",
      "alert_color": "#FA4D30",
      "background_color": "#FFFFFF",
    },
    "dark": {
      "primary_color": "#1054DE",
      "secondary_color": "#292B32",
      "base_color": "#ebecef",
      "base_shade1_color": "#a5a9b5",
      "base_shade2_color": "#6e7487",
      "base_shade3_color": "#40434e",
      "base_shade4_color": "#292b32",
      "alert_color": "#FA4D30",
      "background_color": "#191919",
    }
  }
```

## Configuration ID of Page, Component, and Element

We support three different levels - **Page, Component,** and **Element**. The format is like `page_id/component_id/element_id`.&#x20;

**Page ID -** We use `post` suffix and placed at first, it will look like `camera_page/*/*`

**Component ID** - We use `component` suffix and placed in the middle, it will look like `*/comment_component/*`

**Element ID** - We use no suffix and placed at last, it will look like `*/*/close_button`

## Customizing Page

You can override Global Theme for a specific page with the desired value like below

```json
"camera_page/*/*": {
  "theme": {
    "light": {
      "primary_color": "#1054DE",
      "secondary_color": "#292B32",
      "base_color": "#292b32",
      "base_shade1_color": "#636878",
      "base_shade2_color": "#898e9e",
      "base_shade3_color": "#a5a9b5",
      "base_shade4_color": "#ebecef",
      "alert_color": "#FA4D30",
      "background_color": "#FFFFFF",
    },
    "dark": {
      "primary_color": "#1054DE",
      "secondary_color": "#292B32",
      "base_color": "#ebecef",
      "base_shade1_color": "#a5a9b5",
      "base_shade2_color": "#6e7487",
      "base_shade3_color": "#40434e",
      "base_shade4_color": "#292b32",
      "alert_color": "#FA4D30",
      "background_color": "#191919",
    }
  }
}
```

#### Allowed Page IDs

These are the available Page IDs

<pre class="language-json"><code class="lang-json"><strong>"select_target_page/*/*"
</strong><strong>"camera_page/*/*"
</strong>"creat_story_page/*/*"
"story_page/*/*"
</code></pre>

## Customizing Component

You can also override Global Theme for a specific component with the desired value like below

```json
"*/edit_comment_component/*": {
  "theme": {
    "light": {
      "primary_color": "#1054DE",
      "secondary_color": "#292B32",
      "base_color": "#292b32",
      "base_shade1_color": "#636878",
      "base_shade2_color": "#898e9e",
      "base_shade3_color": "#a5a9b5",
      "base_shade4_color": "#ebecef",
      "alert_color": "#FA4D30",
      "background_color": "#FFFFFF",
    },
    "dark": {
      "primary_color": "#1054DE",
      "secondary_color": "#292B32",
      "base_color": "#ebecef",
      "base_shade1_color": "#a5a9b5",
      "base_shade2_color": "#6e7487",
      "base_shade3_color": "#40434e",
      "base_shade4_color": "#292b32",
      "alert_color": "#FA4D30",
      "background_color": "#191919",
    }
  }
}
```

## Allowed Component IDs

These are the available Component IDs

```json
"*/edit_comment_component/*"
"*/comment_tray_component/*"
"*/story_tab_component/*"
```

## Customizing Element

You can specify `background_color` for an element, and `icon` if that element has an image icon.

```json
"create_story_page/*/aspect_ratio_button": {
    "aspect_ratio_icon": "aspect_ratio.png",
    "background_color": "#80000000"
}
```

#### Allowed Component IDs

These are the available Component IDs

```json
"select_target_page/*/back_button"
"camera_page/*/close_button"
"create_story_page/*/back_button"
"create_story_page/*/aspect_ratio_button"
"create_story_page/*/story_hyperlink_button"
"create_story_page/*/hyper_link"
"create_story_page/*/share_story_button"
"story_page/*/progress_bar"
"story_page/*/overflow_menu"
"story_page/*/close_button"
"story_page/*/story_impression_button"
"story_page/*/story_comment_button"
"story_page/*/story_reaction_button"
"story_page/*/create_new_story_button"
"story_page/*/speaker_button"
"*/edit_comment_component/cancel_button"
"*/edit_comment_component/save_button"
"*/hyper_link_config_component/*"
"*/hyper_link_config_component/done_button"
"*/hyper_link_config_component/cancel_button"
"*/story_tab_component/story_ring"
"*/story_tab_component/create_new_story_button"
"*/*/close_button"
```

## Excluding page, component, or element

You can exclude UI elements by specifying their config id in `excludes` in the configuration file.

Example: Excluding the aspect ratio button from the Story Draft page

```json
"excludes": [
    "create_story_page/*/aspect_ratio_button"
]
```
