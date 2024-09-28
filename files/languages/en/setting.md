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

- For random Blueprints, go to ./files/favorite and add your own configurations:

```py
actions.yaml: Actions
artists.yaml: Painting style
characters.yaml: role
emotions.yaml: Emoticons
negative.yaml: Negative
prefixes.yaml: Quality word
stains.yaml: stains
surroundings.yaml scene
```
