### Other Configurations:

About random pictures, please put the prompt files(e.g.: example.txt, including: prompt) into this directory `./files/prompt`

```
e.g.:
.\files
  └---\prompt
        └---可莉.txt -> file contents: tianliang duohe fangdongye, loli, klee_(genshin_impact)
        └---loli.txt -> file contents: {{{loli}}}
        └---114514.txt -> file contents: {henghengheng aaaaa}
```

- Regarding Pixiv upload, you need to place the selected images or folders to upload in the same directory, for example `./output/pixiv`.

```
For example:
.\output
  └---\pixiv
        └---7589641258_GenshinImpact_可莉.png -> Note: The image name follows the format: seed_source_character.png. Tags will be added based on generation information, source, and character, with the character as the title.
        └---6594641258dwuibuib_None_None.png  -> Note: The image name follows the format: content_None_None.png. Tags will be added based on generation information, with None as the title.
        └---拉菲.png                          -> Note: Such images may cause errors. Don't worry, if you use images generated entirely by this project, the generated image names will all adhere to the standard format.
        └---\Nahida                           -> Note: You can treat folders as image groups, meaning one uploaded work contains multiple images.
              └---5264942125_GenshinImpact_纳西妲.png
              └---4351819919_GenshinImpact_纳西妲.png
```

About random blue pictures, you can add more at the correct position by your self:

```json
{
  "artists": {
    ...,
    "belief": {
      "0.6(probability of extracting art style below, probability here is 1-0.6)": {
        "Art Style(Your preferred art style)": [
          "balabala...",
          0(whether to enable sm, 1 for enable, 0 for disable),
          6.3(relevance of prompts, if set to 0, it will read from the .env file configuration)
        ]
      },
      "0.3(probability of extracting art style below, probability here is 0.6-0.3)": {
        "Art Style(Your preferred art style)": [
          "balabala...",
          0(whether to enable sm, 1 for enable, 0 for disable),
          6.3(relevance of prompts, if set to 0, it will read from the .env file configuration)
        ]
      }
    },
    ...
  },
  "negative_prompt": {
    ...,
    "belief": [
      "prompt(negative prompts)"
    ]
  },
  "character": {
    "Game(Group of characters)": {
      "name(Character name)": [
        "tag1(description of this character)",
        "tag2, tag3(can be single or a series)"
      ]
    }
  },
  "R18": {
    "Action": {
      "Big Breast Action": {
        "name(Action name)": [
          "tag1(description of this action)",
          "tag2, tag3(can be single or a series)"
        ]
      },
      "Ordinary Action": {
        "name(Action name)": [
          "tag1(description of this action)",
          "tag2, tag3(can be single or a series)"
        ]
      }
    },
    "Expression": {
      "Oral Expression": {
        "name(Expression name)": [
          "tag1(description of this expression)",
          "tag2, tag3(can be single or a series)"
        ]
      },
      "Ordinary Expression": {
        "name(Expression name)": [
          "tag1(description of this expression)",
          "tag2, tag3(can be single or a series)"
        ]
      }
    },
    "Scene": {
      "Scene Only": {
        "name(Scene name)": [
          "tag1(description of this scene)",
          "tag2, tag3(can be single or a series)"
        ]
      },
      ...
    },
    ...
  },
  "labels": {
    "Game(Corresponding to the added sources above)": {
      "name(Corresponding to the added characters above)": [
        "char_name(Tags added to this character when uploading to Pixiv)",
        "char_jp_name(Tags added to this character when uploading to Pixiv)"
      ]
    },
    "description": {
      "tag (A certain prompt word)": [
        "tag_label(Tags added to this prompt word when uploading to Pixiv)"
      ]
    }
  }
}
```
