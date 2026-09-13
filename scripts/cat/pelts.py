import random
from random import choice
from re import sub

import i18n
import colorsys # Modded: allows conversion betweeen rgb and hsv

import scripts.game_structure.screen_settings
from scripts.cat.enums import CatAge
from scripts.cat.sprites.load_sprites import sprites
from scripts.game_structure import constants
from scripts.game_structure.localization import get_lang_config
from scripts.events_module.text_adjust import adjust_list_text


class Pelt:
    # POSES
    all_poses = sprites.POSE_DATA["poses"]
    newborn_poses = [x for x in all_poses if "newborn" in x]
    kitten_poses = [x for x in all_poses if "kitten" in x and "sick" not in x]
    adolescent_long_poses = [
        x for x in all_poses if "adolescent_long" in x and "sick" not in x
    ]
    adolescent_short_poses = [
        x
        for x in all_poses
        if "adolescent" in x and "long" not in x and "sick" not in x
    ]
    adult_short_poses = [
        x
        for x in all_poses
        if "adult_short" in x and "para" not in x and "sick" not in x
    ]
    adult_long_poses = [
        x
        for x in all_poses
        if "adult_long" in x and "para" not in x and "sick" not in x
    ]
    senior_poses = [x for x in all_poses if "senior" in x and "sick" not in x]

    # PELT LENGTH
    pelt_length = ["short", "medium", "long"]

    # PELT COLOURS
    all_pelt_colours: list = []
    ginger_colours: list = []
    black_colours: list = []
    white_colours: list = []
    brown_colours: list = []

    all_pelt_colours.extend(
        list(sprites.GENERATION_GROUP_DATA["pelts"]["colors"].keys())
    )
    for colour in sprites.GENERATION_GROUP_DATA["pelts"]["colors"]:
        group = sprites.GENERATION_GROUP_DATA["pelts"]["colors"][colour]

        if group == "white":
            white_colours.append(colour)
        elif group == "black":
            black_colours.append(colour)
        elif group == "ginger":
            ginger_colours.append(colour)
        elif group == "brown":
            brown_colours.append(colour)
        else:
            # Default
            brown_colours.append(colour)

    # colour categories
    colour_categories: list[list] = [
        ginger_colours,
        black_colours,
        white_colours,
        brown_colours,
    ]

    # PELT PATTERNS
    pelt_patterns: list = list(
        sprites.GENERATION_GROUP_DATA["pelts"]["pattern_types"].keys()
    )

    # pattern categories
    pelt_categories: dict = {}
    for key, value in sprites.GENERATION_GROUP_DATA["pelts"]["pattern_types"].items():
        if value in pelt_categories:
            pelt_categories[value].append(key)
        else:
            pelt_categories[value] = [key]

    # individual pattern categories
    tabbies: list = pelt_categories["tabbies"]
    spotted: list = pelt_categories["spotted"]
    plain: list = pelt_categories["plain"]
    exotic: list = pelt_categories["exotic"]
    torties: list = pelt_categories["torties"]

    """
    # PELT SPRITE NAMES
    # pelt name used in save files: pelt's spritesheet
    pattern_sprite_names: dict = {}
    for sheet, names in sprites.PELT_DATA["spritesheet"].items():
        for name in names:
            pattern_sprite_names.update({name: sheet})
    pattern_sprite_names.update(
        {
            "Tortie": None,
            "Calico": None,
        }
    )
    """

    # TORTIE PATCHES
    tortie_patches: list = list(sprites.TORTIE_PATCH_COMBOS.keys())
    for sprite_list in sprites.TORTIE_DATA["sprite_list"]:
        tortie_patches.extend(sprite_list)

    # WHITE MARKINGS
    little_white: list = list(sprites.WHITE_PATCH_COMBOS.get("little", {}).keys())
    for sprite_list in sprites.WHITE_LITTLE_DATA["sprite_list"]:
        little_white.extend(sprite_list)
    mid_white: list = list(sprites.WHITE_PATCH_COMBOS.get("mid", {}).keys())
    for sprite_list in sprites.WHITE_MID_DATA["sprite_list"]:
        mid_white.extend(sprite_list)
    high_white: list = list(sprites.WHITE_PATCH_COMBOS.get("high", {}).keys())
    for sprite_list in sprites.WHITE_HIGH_DATA["sprite_list"]:
        high_white.extend(sprite_list)
    mostly_white: list = list(sprites.WHITE_PATCH_COMBOS.get("mostly", {}).keys())
    for sprite_list in sprites.WHITE_MOSTLY_DATA["sprite_list"]:
        # have to remove FULLWHITE as it's handled special
        mostly_white.extend([x for x in sprite_list if x != "FULLWHITE"])
        
    vitiligo_markings: list = []
    for sprite_list in sprites.WHITE_VITILIGO_DATA["sprite_list"]:
        vitiligo_markings.extend(sprite_list)
    point_markings: list = []
    for sprite_list in sprites.WHITE_POINT_DATA["sprite_list"]:
        point_markings.extend(sprite_list)

    #Modded: all markings list
    valid_white_markings: list = little_white + mid_white + high_white + mostly_white 


    # EYES
    all_eye_colours: list = []
    yellow_eyes: list = []
    green_eyes: list = []
    blue_eyes: list = []
    for sprite_list in sprites.EYE_DATA["sprite_list"]:
        all_eye_colours.extend(sprite_list.keys())
        for colour in sprite_list:
            if sprite_list[colour] == "yellow":
                yellow_eyes.append(colour)
            elif sprite_list[colour] == "green":
                green_eyes.append(colour)
            elif sprite_list[colour] == "blue":
                blue_eyes.append(colour)

    # SKIN
    skin_sprites: list = []
    for sprite_list in sprites.SKIN_DATA["sprite_list"]:
        skin_sprites.extend(sprite_list)

    # SCARS
    # bite scars by @wood pank on discord
    general_scars = []
    for sprite_list in sprites.SCAR_DATA["sprite_list"]:
        general_scars.extend(sprite_list)

    missing_part_scars = []
    for sprite_list in sprites.SCAR_MISSING_PART_DATA["sprite_list"]:
        missing_part_scars.extend(sprite_list)

    all_scars = general_scars + missing_part_scars

    # ACCESSORIES
    # make sure to add plural and singular forms of new accs to accessories.en.json so that they will display nicely

    # all acc sprites are labeled as occupying a specific part of the cat sprite and then appended into these three lists
    # collar_accessories are presumed to all occupy the neck area and are treated as the fourth of these lists
    tail_accessories = []
    body_accessories = []
    head_accessories = []
    paw_accessories = []

    # here we create the master lists of each accessory type
    plant_accessories = []
    for sprite_list in sprites.PLANT_DATA["sprite_list"]:
        plant_accessories.extend(sprite_list)
        for sprite in sprite_list:
            if sprite_list[sprite] == "tail":
                tail_accessories.append(sprite)
            elif sprite_list[sprite] == "body":
                body_accessories.append(sprite)
            elif sprite_list[sprite] == "head":
                body_accessories.append(sprite)
            elif sprite_list[sprite] == "paw":
                paw_accessories.append(sprite)

    wild_accessories = []
    for sprite_list in sprites.WILD_DATA["sprite_list"]:
        wild_accessories.extend(sprite_list)
        for sprite in sprite_list:
            if sprite_list[sprite] == "tail":
                tail_accessories.append(sprite)
            elif sprite_list[sprite] == "body":
                body_accessories.append(sprite)
            elif sprite_list[sprite] == "head":
                body_accessories.append(sprite)
            elif sprite_list[sprite] == "paw":
                paw_accessories.append(sprite)

    collar_accessories = []
    collar_styles = []
    if sprites.COLLAR_DATA["palette_map"]:
        for style_type in sprites.COLLAR_DATA["style_data"]:
            for style, color_list in style_type.items():
                collar_styles.append(style)
                for colour in color_list:
                    collar_accessories.append(f"{style}_{colour}")
    else:
        for sprite_list in sprites.COLLAR_DATA["sprite_list"]:
            collar_accessories.extend(sprite_list)

    # this is used for acc-giving events, only change if you're adding a new category tag to the event filter
    # adding a category here will automatically update the event editor's options
    acc_categories = {
        "PLANT": plant_accessories,
        "WILD": wild_accessories,
        "COLLAR": collar_accessories,
    }

    """Holds all appearance information for a cat. """

    def __init__(
        self,
        name: str = "SingleColour",
        length: str = "short",
        colour: str = "WHITE",
        white_patches: str = None,
        eye_color: str = "BLUE",
        eye_colour2: str = None,
        tortie_base: str = None,
        tortie_colour: str = None,
        tortie_marking: str = None,
        tortie_pattern: str = None,
        vitiligo: str = None,
        points: str = None,
        accessory: list = None,
        paralyzed: bool = False,
        opacity: int = 100,
        scars: list = None,
        tint: str | None = None,
        skin: str = "BLACK",
        white_patches_tint: str | None = None,
        newborn_sprite: str = None,
        kitten_sprite: str = None,
        adol_sprite: str = None,
        adult_sprite: str = None,
        senior_sprite: str = None,
        para_adult_sprite: str = None,
        reverse: bool = False,
    ) -> None:
        self.name = name
        self.colour = colour
        self.white_patches = white_patches
        self.eye_colour = eye_color
        self.eye_colour2 = eye_colour2
        self.tortie_base = tortie_base
        self.tortie_marking = tortie_marking
        self.tortie_pattern = tortie_pattern
        self.tortie_colour = tortie_colour
        self.vitiligo = vitiligo
        self.length = length
        self.points = points
        self.rebuild_sprite = True
        self._accessory = accessory
        self._paralyzed = paralyzed
        self.opacity = opacity
        self._scars = (
            tuple(scars)
            if isinstance(scars, list)
            else scars
            if isinstance(scars, tuple)
            else tuple()
        )
        self.tint = tint
        self.white_patches_tint = white_patches_tint
        self.screen_scale = scripts.game_structure.screen_settings.screen_scale

        # converting old pose numbers into names
        if any(
            isinstance(x, int) or x is None
            for x in [
                newborn_sprite,
                kitten_sprite,
                adol_sprite,
                adult_sprite,
                senior_sprite,
                para_adult_sprite,
            ]
        ):
            # DO NOT CHANGE THIS: this is meant to convert old saves and should not be updated with new pose additions
            self.cat_sprites = {
                "kitten": kitten_sprite if kitten_sprite is not None else 0,
                "adolescent": adol_sprite if adol_sprite is not None else 3,
                "young adult": adult_sprite if adult_sprite is not None else 6,
                "adult": adult_sprite if adult_sprite is not None else 6,
                "senior adult": adult_sprite if adult_sprite is not None else 6,
                "senior": senior_sprite if senior_sprite is not None else 12,
                "para_adult": para_adult_sprite,
                "newborn": 20,
            }
            for age, pose in self.cat_sprites.items():
                # we only need to convert if it's using the old sprite pose numbers
                if not isinstance(pose, int):
                    continue

                # convert paras
                if age == "para_adult":
                    if self.length == "long":
                        self.cat_sprites[age] = "para_adult_long0"
                    else:
                        self.cat_sprites[age] = "para_adult_short0"
                    continue

                elif age == CatAge.NEWBORN:
                    self.cat_sprites[age] = (
                        "newborn2" if "newborn2" in self.newborn_poses else "newborn0"
                    )
                    continue
                elif age == CatAge.KITTEN:
                    # since these were at the top of the sheet, the pose nums were 0, 1, 2. thus they'll naturally match this fstring
                    self.cat_sprites[age] = f"kitten{pose if pose in (0, 1, 2) else 0}"
                    continue
                elif age == CatAge.ADOLESCENT:
                    if self.length == "long":
                        fur = "long"
                    else:
                        fur = "short"
                    if pose == 3:
                        self.cat_sprites[age] = f"adolescent_{fur}0"
                    elif pose == 4:
                        self.cat_sprites[age] = f"adolescent_{fur}1"
                    elif pose == 5:
                        self.cat_sprites[age] = f"adolescent_{fur}2"
                    else:
                        self.cat_sprites[age] = choice(
                            (
                                f"adolescent_{fur}0",
                                f"adolescent_{fur}1",
                                f"adolescent_{fur}2",
                            )
                        )
                elif age in (CatAge.YOUNG_ADULT, CatAge.ADULT, CatAge.SENIOR_ADULT):
                    if pose in (0, 9):
                        self.cat_sprites[age] = "adult_long0"
                    elif pose in (1, 10):
                        self.cat_sprites[age] = "adult_long1"
                    elif pose in (2, 11):
                        self.cat_sprites[age] = "adult_long2"
                    elif pose == 6:
                        self.cat_sprites[age] = "adult_short0"
                    elif pose == 7:
                        self.cat_sprites[age] = "adult_short1"
                    elif pose == 8:
                        self.cat_sprites[age] = "adult_short2"
                    else:
                        if self.length == "long":
                            self.cat_sprites[age] = choice(
                                ("adult_long0", "adult_long1", "adult_long2")
                            )
                        else:
                            self.cat_sprites[age] = choice(
                                ("adult_short0", "adult_short1", "adult_short2")
                            )

                elif age == CatAge.SENIOR:
                    if pose in (3, 12):
                        self.cat_sprites[age] = "senior0"
                    elif pose in (4, 13):
                        self.cat_sprites[age] = "senior1"
                    elif pose in (5, 14):
                        self.cat_sprites[age] = "senior2"
                    else:
                        self.cat_sprites[age] = choice(
                            ("senior0", "senior1", "senior2")
                        )

        # now for the updating handling of pose name strings
        else:
            adult_sprite = (
                adult_sprite
                if adult_sprite is not None
                and (
                    adult_sprite in self.adult_short_poses
                    or adult_sprite in self.adult_long_poses
                )
                else "adult_short0"
            )

            if adol_sprite in ("adolescent0", "adolescent1", "adolescent2"):
                if self.length == "long":
                    adol_sprite = random.choice(self.adolescent_long_poses)
                else:
                    adol_sprite = f"adolescent_short{adol_sprite[-1]}"

            self.cat_sprites = {
                "newborn": newborn_sprite
                if newborn_sprite is not None and newborn_sprite in self.newborn_poses
                else "newborn0",
                "kitten": kitten_sprite
                if kitten_sprite is not None and kitten_sprite in self.kitten_poses
                else "kitten0",
                "adolescent": adol_sprite
                if adol_sprite is not None
                and (
                    adol_sprite in self.adolescent_short_poses
                    or adol_sprite in self.adolescent_long_poses
                )
                else "adolescent_short0",
                "young adult": adult_sprite,
                "adult": adult_sprite,
                "senior adult": adult_sprite,
                "senior": senior_sprite
                if senior_sprite is not None and senior_sprite in self.senior_poses
                else "senior0",
                "para_adult": para_adult_sprite
                if para_adult_sprite is not None
                else "para_adult_short0",
                "para_young": "para_young0",
            }

        self.reverse = reverse
        self.skin = skin

    @property
    def accessory(self):
        return self._accessory

    @accessory.setter
    def accessory(self, val):
        self.rebuild_sprite = True
        self._accessory = val

    @property
    def scars(self):
        return self._scars

    @scars.setter
    def scars(self, val):
        self.rebuild_sprite = True
        self._scars = val

    @property
    def paralyzed(self):
        return self._paralyzed

    @paralyzed.setter
    def paralyzed(self, val):
        self.rebuild_sprite = True
        self._paralyzed = val

    @staticmethod
    def generate_new_pelt(gender: str, parents: tuple = (), age: str = "adult"):
        new_pelt = Pelt()

        pelt_white = new_pelt.init_pattern_color(parents, gender)
        #new_pelt.init_white_patches(pelt_white, parents) Modded: removed use of white patch function
        new_pelt.init_sprite()
        new_pelt.init_scars(age)
        new_pelt.init_accessories(age)
        new_pelt.init_eyes(parents)
        new_pelt.init_pattern() #This handles torties, may edit?
        #new_pelt.init_tint() #Modded: removed use of tint function
        
#Modded: set tint
        if parents:   # If the cat has parents, use inheritance to decide tint.
            
            
            # Set up variables
            par_tints = []
            par_rgb = []
            kit_tint = [0,0,0]
            kit_white_tint = None
            new_pelt.white_patches = None
            
            # For each parent, add tint to list and add RGB value of tint to RGB sum
            for p in parents:
                if p:
                    #Set parent tint to base tint
                    parent_tint = p.pelt.tint
                    
                    # If parent has 2nd color, choose random color for tint
                    if p.pelt.white_patches:
                        parent_tint = random.choice([p.pelt.tint, p.pelt.white_patches_tint])
                        
                    # Convert color to hsv and add hsv to parent tints lists
                    hsv_value = colorsys.rgb_to_hsv(parent_tint[0]/255, parent_tint[1]/255, parent_tint[2]/255,)
                    par_tints.append(hsv_value)
                    par_rgb.append(parent_tint)
                    
                    
            #If parent values are same, remove one(makes multicolor and gradients not happen if same color parents)
            if len(par_tints) == 2:
                if par_tints[0] == par_tints[1]:
                    par_tints.pop()
                    
            print(f'Parent hsv tints:{par_tints}  RGB: {par_rgb}') #print for testing
            
            # 1/chance chance to be multicolor if parent tints are different
            if (len(par_tints) == 2)  and (constants.CONFIG["cat_generation"]["multi_col_chance"] > 0) and (random.randint(1, constants.CONFIG["cat_generation"]["multi_col_chance"]) == 1):
                # Python evaluates and statements in order so if config is 0 it won't bother with randint and thus not crast from randint(0,0)
                new_pelt.name = "TwoColour"
                kit_white_tint = [0,0,0]
                
                white_marking = None
                vit_chance = max(
                    constants.CONFIG["cat_generation"]["vit_chance"], 0
                )
                if not random.getrandbits(vit_chance): # Roll to see if markings are vitiligo style
                    white_marking = choice(Pelt.vitiligo_markings)
                else: #If not vit, roll for if point
                    if not random.getrandbits(
                        constants.CONFIG["cat_generation"]["random_point_chance"]
                    ):
                        white_marking = choice(Pelt.point_markings)
                        
                    else: # If neither, half chance to pick white patch and half chance to pick tortie patch
                        white_marking = random.choice(random.choice([Pelt.valid_white_markings, Pelt.tortie_patches]))
                
                
                
                new_pelt.white_patches = white_marking
                
                # Kit gets both parents' colors, half chance for either orientation
                if random.randint(1, 2) == 1:
                    kit_tint = par_tints[0]
                    kit_white_tint = par_tints[1]
                else: 
                    kit_tint = par_tints[1]
                    kit_white_tint = par_tints[0]
                print(f' multi: {kit_tint} {kit_white_tint} {new_pelt.white_patches} ')
                
            
            else: #Set tint to merged version with no patches
                
                # Make sure no patches
                kit_white_tint = None
                new_pelt.white_patches = None
                
                # Variable that determines where kit color will be relative to parent's
                # Move into for loop to disconnect hsv rolls
                inbetween_percent = constants.CONFIG["cat_generation"]["inbetween_percent"]
                #print(inbetween_percent)
                try:
                    if inbetween_percent[0] == 1224: #If ABX uniform
                        inbetween = random.choice([i/(inbetween_percent[3]) for i in range(inbetween_percent[1],inbetween_percent[2])])
                        
                    elif inbetween_percent[0] == 0.1415: # If normal dist
                        inbetween = random.gauss(inbetween_percent[1], inbetween_percent[2])
                        
                    else: #If normal pick random value from list:
                        inbetween =  random.choice(inbetween_percent)
                    
                except: #If invalid, default to exact middle
                    print("There was an error with reading inbetween_percent." )
                    inbetween =  0.5
                
                
                
                
                
                
                # For each value
                for index in [0,1,2]:
                    
                    grayscale_par = None
                    #If checking hue and either parent has 0 saturation(if both do doesn't matter cause hue won't show in any kits)
                    if len(par_tints) == 2 and index == 0:
                        if par_tints[0][1] == 0: #If first parent has 0 sat
                            grayscale_par = "first"
                                
                        if par_tints[1][1] == 0: #If 2nd parent has 0 sat
                            if grayscale_par == "first":
                                grayscale_par = "both"
                            else:
                                grayscale_par = "second"
                    
                    # Direct Inherit: 1/chance chance per color value to be a copy of one of parent's if not hue and both parents 0 sat
                    if (not random.randint(0, constants.CONFIG["cat_generation"]["direct_inheritance"]) and (not grayscale_par == "both")):
                    
                        if grayscale_par == None: # if no grayscale parents/not on hue, pick random
                            kit_tint[index] = choice(par_tints)[index]
                        elif grayscale_par == "first": # If are on hue and first parent is grayscale, pick second's hue
                            kit_tint[index] = par_tints[1][index]
                        else: # If are on hue and 2nd parent is grayscale, pick 1st's hue
                            kit_tint[index] = par_tints[0][index]
                            
                        #print(f' {index} {choice(par_tints)}  parent to inherit from: {kit_tint[index]}')
                        
                        
                    else:
                        
                        if(len(par_tints) == 2): # If two parents, get max and min
                            
                            #If hue and wrapped hue would be shorter, set min to higher value and max to lower value + 1
                            if (index == 0) and (abs(par_tints[0][0] - par_tints[1][0]) > 0.5):
                                min_par_val = max(par_tints[0][index], par_tints[1][index])
                                max_par_val = min(par_tints[0][index], par_tints[1][index])+1
                            else:
                                min_par_val = min(par_tints[0][index], par_tints[1][index])
                                max_par_val = max(par_tints[0][index], par_tints[1][index])
                            
                            #print(f" {index} min: {min_par_val}  max: {max_par_val} ")
                                
                            #Ignore hues of parents with 0 saturation 
                            if grayscale_par == "first": #If first parent has 0 sat,
                                min_par_val = max_par_val = par_tints[1][0]  #Set hue to that of second parent
                            
                            elif grayscale_par == "second": #If 2nd parent has 0 sat,
                                min_par_val = max_par_val = par_tints[0][0]  #Set hue to that of 1st parent
                                
                            # Difference = max-min
                            diff_par_val = max_par_val - min_par_val
                            
                        else: # If one parent, sex max+min to same value and difference to none
                            min_par_val = max_par_val = par_tints[0][index]
                            diff_par_val = 0
                        
                        # Set kit value
                        kit_tint[index] = (min_par_val + ( diff_par_val* inbetween))
                        
                        #print(f" {index} min: {min_par_val}  max: {max_par_val} diff: {diff_par_val} kit: { kit_tint[index]}")
                        
                        # Fix for wrapping hues
                        if (index == 0) and (kit_tint[index]) >1:
                            kit_tint[index] = kit_tint[index] -1
                        
                        
                        
                    # Correct if any values go too extreme
                    if kit_tint[index] <0: kit_tint[index] = 0
                    if kit_tint[index] >1: kit_tint[index] = 1
                    #print(f'value: {kit_tint[index]}')
                    
            #print(f'final hsv tint: {kit_tint}')
                
            # Convert hsv to rgb
            kit_tint = [round(i * 255) for i in colorsys.hsv_to_rgb(kit_tint[0], kit_tint[1], kit_tint[2])]
            if kit_white_tint:
                kit_white_tint = [round(i * 255) for i in colorsys.hsv_to_rgb(kit_white_tint[0], kit_white_tint[1], kit_white_tint[2])]
            
            
            
            #print(f'final rgb tint: {kit_tint}')
            
            
            # Set pelt tint to RGB
            new_pelt.tint = tuple( kit_tint )
            if kit_white_tint:
                new_pelt.white_patches_tint = tuple( kit_white_tint )
            
            
            
        else:         # If no parents, random RGB and no 2ndary color
            kit_white_tint = None
            new_pelt.white_patches = None
            
            if constants.CONFIG["cat_generation"]["tint_gen_type"] == 1: #Set parentless cats to have completely random color
                new_pelt.tint = tuple( [random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)] )
                
            elif constants.CONFIG["cat_generation"]["tint_gen_type"] == 2: #Set parentless cats to have color ftom set ranges
                hue = random.uniform(constants.CONFIG["cat_generation"]["hue_range"][0], constants.CONFIG["cat_generation"]["hue_range"][1])
                satur = random.uniform(constants.CONFIG["cat_generation"]["sat_range"][0], constants.CONFIG["cat_generation"]["sat_range"][1])
                valu = random.uniform(constants.CONFIG["cat_generation"]["val_range"][0], constants.CONFIG["cat_generation"]["val_range"][1])
                
                new_pelt.tint = [round(i * 255) for i in colorsys.hsv_to_rgb(hue, satur, valu)]
                #print(f'HSV: {[round(hue, 2), round(satur, 2), round(valu, 2)]}')
            
            else: #Else, pull from RGB list
                
                if constants.CONFIG["cat_generation"]["bright_mod"] >= 1.0: #If no eye sensitivity reduction, just pick color
                    new_pelt.tint = tuple( random.choice(constants.CONFIG["cat_generation"]["RGB_tints"]) )
                
                else: #If sensitivity setting on, reduce satur+valu
                    rgb_col = random.choice(constants.CONFIG["cat_generation"]["RGB_tints"])
                    [hue, satur, valu] = colorsys.rgb_to_hsv(rgb_col[0]/255, rgb_col[1]/255, rgb_col[2]/255)
                    bright_mod = constants.CONFIG["cat_generation"]["bright_mod"]
                    new_pelt.tint = tuple([round(i * 255) for i in colorsys.hsv_to_rgb(hue, satur*bright_mod, valu*bright_mod)])

        #Modded: print statement
        #print(f'final tint: {new_pelt.tint}')
        

        return new_pelt

    def check_and_convert(self, convert_dict):
        """Checks for old-type properties for the appearance-related properties
        that are stored in Pelt, and converts them. To be run when loading a cat in."""

        # First, convert from some old names that may be in white_patches.
        if self.white_patches == "POINTMARK":
            self.white_patches = "SEALPOINT"
        elif self.white_patches == "PANTS2":
            self.white_patches = "PANTSTWO"
        elif self.white_patches == "ANY2":
            self.white_patches = "ANYTWO"
        elif self.white_patches == "VITILIGO2":
            self.white_patches = "VITILIGOTWO"

        if self.vitiligo == "VITILIGO2":
            self.vitiligo = "VITILIGOTWO"

# Don't move point/vit white patches
#         # Move white_patches that should be in vit or points.
#         if self.white_patches in Pelt.vitiligo_markings:
#             self.vitiligo = self.white_patches
#             self.white_patches = None
#         elif self.white_patches in Pelt.point_markings:
#             self.points = self.white_patches
#             self.white_patches = None

        if self.tortie_pattern and "tortie" in self.tortie_pattern:
            self.tortie_pattern = sub("tortie", "", self.tortie_pattern.lower())
            if self.tortie_pattern == "solid":
                self.tortie_pattern = "single"

        if self.white_patches in convert_dict["old_creamy_patches"]:
            self.white_patches = convert_dict["old_creamy_patches"][self.white_patches]
            self.white_patches_tint = "darkcream"
        elif self.white_patches in ("SEPIAPOINT", "MINKPOINT", "SEALPOINT"):
            self.white_patches_tint = "none"

        # Eye Color Convert Stuff
        if self.eye_colour == "BLUE2":
            self.eye_colour = "COBALT"
        if self.eye_colour2 == "BLUE2":
            self.eye_colour2 = "COBALT"

        if self.eye_colour in ("BLUEYELLOW", "BLUEGREEN"):
            if self.eye_colour == "BLUEYELLOW":
                self.eye_colour2 = "YELLOW"
            elif self.eye_colour == "BLUEGREEN":
                self.eye_colour2 = "GREEN"
            self.eye_colour = "BLUE"

        if self.tortie_marking in convert_dict["old_tortie_patches"]:
            old_pattern = self.tortie_marking
            self.tortie_marking = convert_dict["old_tortie_patches"][old_pattern][1]

            # If the pattern is old, there is also a chance the base color is stored in
            # tortie_colour. That may be different from the pelt color ("main" for torties)
            # generated before the "ginger-on-ginger" update. If it was generated after that update,
            # tortie_colour and pelt_colour will be the same. Therefore, let's also re-set the pelt color
            self.colour = self.tortie_colour
            self.tortie_colour = convert_dict["old_tortie_patches"][old_pattern][0]

        if self.tortie_marking == "MINIMAL1":
            self.tortie_marking = "MINIMALONE"
        elif self.tortie_marking == "MINIMAL2":
            self.tortie_marking = "MINIMALTWO"
        elif self.tortie_marking == "MINIMAL3":
            self.tortie_marking = "MINIMALTHREE"
        elif self.tortie_marking == "MINIMAL4":
            self.tortie_marking = "MINIMALFOUR"

        if self.accessory is None:
            self.accessory = tuple()
        elif isinstance(self.accessory, str):
            self.accessory = tuple([self.accessory])

        new_acc_list = []
        for acc in self.accessory:
            if acc in convert_dict["collar_map"]:
                new_acc_list.append(convert_dict["collar_map"][acc])
            else:
                new_acc_list.append(acc)
        self.accessory = tuple(new_acc_list)

    def init_eyes(self, parents):
        """Sets eye color for this cat's pelt. Takes parents' eye colors into account.
        Heterochromia is possible based on the white-ness of the pelt, so the pelt color and white_patches must be
        set before this function is called.

        :param parents: List[Cat] representing this cat's parents

        :return: None
        """
        if not parents:
            self.eye_colour = choice(Pelt.all_eye_colours)
        else:
            self.eye_colour = choice(
                [i.pelt.eye_colour for i in parents] + [choice(Pelt.all_eye_colours)]
            )

        # White patches must be initialized before eye color.
        num = constants.CONFIG["cat_generation"]["base_heterochromia"]
        if (
            self.white_patches in Pelt.high_white
            or self.white_patches in Pelt.mostly_white
            or self.white_patches == "FULLWHITE"
            or self.colour == "WHITE"
        ):
            num = num - 90
        if self.white_patches == "FULLWHITE" or self.colour == "WHITE":
            num -= 10
        for _par in parents:
            if _par.pelt.eye_colour2:
                num -= 10

        if num < 0:
            num = 1

        if not random.randint(0, num):
            colour_wheel = [Pelt.yellow_eyes, Pelt.blue_eyes, Pelt.green_eyes]
            for colour in colour_wheel[:]:
                if self.eye_colour in colour:
                    colour_wheel.remove(
                        colour
                    )  # removes the selected list from the options
                    self.eye_colour2 = choice(
                        choice(colour_wheel)
                    )  # choose from the remaining two lists
                    break

    def pattern_color_inheritance(self, parents: tuple = (), gender="female"):
        # setting parent pelt categories
        # We are using a set, since we don't need this to be ordered, and sets deal with removing duplicates.
        par_peltlength = set()
        par_peltcolours = set()
        par_peltnames = set()
        par_pelts = []
        par_white = []
        for p in parents:
            if p:
                # Gather pelt color.
                par_peltcolours.add(p.pelt.colour)

                # Gather pelt length
                par_peltlength.add(p.pelt.length)

                # Gather pelt name
                if p.pelt.name in Pelt.torties:
                    par_peltnames.add(p.pelt.tortie_base.capitalize())
                else:
                    par_peltnames.add(p.pelt.name)

                # Gather exact pelts, for direct inheritance.
                par_pelts.append(p.pelt)

                # Gather if they have white in their pelt.
                par_white.append(p.pelt.white)
            else:
                # If order for white patches to work correctly, we also want to randomly generate a "pelt_white"
                # for each "None" parent (missing or unknown parent)
                par_white.append(bool(random.getrandbits(1)))

                # Append None
                # Gather pelt color.
                par_peltcolours.add(None)
                par_peltlength.add(None)
                par_peltnames.add(None)

        # If this list is empty, something went wrong.
        if not par_peltcolours:
            print("Warning - no parents: pelt randomized")
            return self.randomize_pattern_color(gender)

        # There is a 1/10 chance for kits to have the exact same pelt as one of their parents
        if not random.randint(
            0, constants.CONFIG["cat_generation"]["direct_inheritance"]
        ):  # 1/10 chance
            selected = choice(par_pelts)
            self.name = selected.name
            self.length = selected.length
            self.colour = selected.colour
            self.tortie_base = selected.tortie_base
            return selected.white

        # ------------------------------------------------------------------------------------------------------------#
        #   PELT
        # ------------------------------------------------------------------------------------------------------------#

        # Determine pelt.
        weights = [
            0,
            0,
            0,
            0,
        ]  # Weights for each pelt group. It goes: (tabbies, spotted, plain, exotic)
        for p_ in par_peltnames:
            if p_ in Pelt.tabbies:
                add_weight = (50, 10, 5, 7)
            elif p_ in Pelt.spotted:
                add_weight = (10, 50, 5, 5)
            elif p_ in Pelt.plain:
                add_weight = (5, 5, 50, 0)
            elif p_ in Pelt.exotic:
                add_weight = (15, 15, 1, 45)
            elif (
                p_ is None
            ):  # If there is at least one unknown parent, a None will be added to the set.
                add_weight = (35, 20, 30, 15)
            else:
                add_weight = (0, 0, 0, 0)

            for x in range(0, len(weights)):
                weights[x] += add_weight[x]

        # A quick check to make sure all the weights aren't 0
        if all([x == 0 for x in weights]):
            weights = [1, 1, 1, 1]

        # Now, choose the pelt category and pelt
        possible_pelts = [
            Pelt.pelt_categories[x] for x in Pelt.pelt_categories if x != "torties"
        ]
        chosen_pelt = choice(random.choices(possible_pelts, weights=weights, k=1)[0])

        # Tortie chance
        tortie_chance_f = constants.CONFIG["cat_generation"][
            "base_female_tortie"
        ]  # There is a default chance for female tortie
        tortie_chance_m = constants.CONFIG["cat_generation"]["base_male_tortie"]
        for p_ in par_pelts:
            if p_.name in Pelt.torties:
                tortie_chance_f = int(tortie_chance_f / 2)
                tortie_chance_m = tortie_chance_m - 1
                break

        # Determine tortie:
        if gender == "female":
            torbie = random.getrandbits(tortie_chance_f) == 1
        else:
            torbie = random.getrandbits(tortie_chance_m) == 1

        chosen_tortie_base = None
        if torbie:
            # If it is tortie, the chosen pelt above becomes the base pelt.
            chosen_tortie_base = chosen_pelt
            # if chosen_tortie_base in ("TwoColour", "SingleColour"):
            #    chosen_tortie_base = "Single"
            chosen_tortie_base = chosen_tortie_base
            chosen_pelt = random.choice(Pelt.torties)

        # ------------------------------------------------------------------------------------------------------------#
        #   PELT COLOUR
        # ------------------------------------------------------------------------------------------------------------#
        # Weights for each colour group. It goes: (ginger_colours, black_colours, white_colours, brown_colours)
        weights = [0, 0, 0, 0]
        for p_ in par_peltcolours:
            if p_ in Pelt.ginger_colours:
                add_weight = (40, 0, 0, 10)
            elif p_ in Pelt.black_colours:
                add_weight = (0, 40, 2, 5)
            elif p_ in Pelt.white_colours:
                add_weight = (0, 5, 40, 0)
            elif p_ in Pelt.brown_colours:
                add_weight = (10, 5, 0, 35)
            elif p_ is None:
                add_weight = (40, 40, 40, 40)
            else:
                add_weight = (0, 0, 0, 0)

            for x in range(0, len(weights)):
                weights[x] += add_weight[x]

            # A quick check to make sure all the weights aren't 0
            if all([x == 0 for x in weights]):
                weights = [1, 1, 1, 1]

        chosen_pelt_color = choice(
            random.choices(Pelt.colour_categories, weights=weights, k=1)[0]
        )

        # ------------------------------------------------------------------------------------------------------------#
        #   PELT LENGTH
        # ------------------------------------------------------------------------------------------------------------#

        weights = [0, 0, 0]  # Weights for each length. It goes (short, medium, long)
        for p_ in par_peltlength:
            if p_ == "short":
                add_weight = (50, 10, 2)
            elif p_ == "medium":
                add_weight = (25, 50, 25)
            elif p_ == "long":
                add_weight = (2, 10, 50)
            elif p_ is None:
                add_weight = (10, 10, 10)
            else:
                add_weight = (0, 0, 0)

            for x in range(0, len(weights)):
                weights[x] += add_weight[x]

        # A quick check to make sure all the weights aren't 0
        if all([x == 0 for x in weights]):
            weights = [1, 1, 1]

        chosen_pelt_length = random.choices(Pelt.pelt_length, weights=weights, k=1)[0]

        # ------------------------------------------------------------------------------------------------------------#
        #   PELT WHITE
        # ------------------------------------------------------------------------------------------------------------#

        # There are 94 percentage points that can be added by
        # parents having white. If we have more than two, this
        # will keep that the same.
        percentage_add_per_parent = int(94 / len(par_white))
        chance = 3
        for p_ in par_white:
            if p_:
                chance += percentage_add_per_parent

        chosen_white = random.randint(1, 100) <= chance

        # Adjustments to pelt chosen based on if the pelt has white in it or not.
        if chosen_pelt in ("TwoColour", "SingleColour"):
            if chosen_white:
                chosen_pelt = "TwoColour"
            else:
                chosen_pelt = "SingleColour"
        elif chosen_pelt == "Calico":
            if not chosen_white:
                chosen_pelt = "Tortie"

        # SET THE PELT
        self.name = chosen_pelt
        self.colour = chosen_pelt_color
        self.length = chosen_pelt_length
        self.tortie_base = (
            chosen_tortie_base  # This will be none if the cat isn't a tortie.
        )
        return chosen_white

    def randomize_pattern_color(self, gender):
        # ------------------------------------------------------------------------------------------------------------#
        #   PELT
        # ------------------------------------------------------------------------------------------------------------#

        # Determine pelt.
        possible_pelts = [
            Pelt.pelt_categories[x] for x in Pelt.pelt_categories if x != "torties"
        ]
        chosen_pelt = choice(
            random.choices(possible_pelts, weights=(35, 20, 30, 15), k=1)[0]
        )

        # Tortie chance
        # There is a default chance for female tortie, slightly increased for completely random generation.
        tortie_chance_f = constants.CONFIG["cat_generation"]["base_female_tortie"] - 1
        tortie_chance_m = constants.CONFIG["cat_generation"]["base_male_tortie"]
        if gender == "female":
            torbie = random.getrandbits(tortie_chance_f) == 1
        else:
            torbie = random.getrandbits(tortie_chance_m) == 1

        chosen_tortie_base = None
        if torbie:
            # If it is tortie, the chosen pelt above becomes the base pelt.
            chosen_tortie_base = chosen_pelt
            # if chosen_tortie_base in ("TwoColour", "SingleColour"):
            #    chosen_tortie_base = "Single"
            chosen_tortie_base = chosen_tortie_base
            chosen_pelt = random.choice(Pelt.torties)

        # ------------------------------------------------------------------------------------------------------------#
        #   PELT COLOUR
        # ------------------------------------------------------------------------------------------------------------#

        chosen_pelt_color = choice(random.choices(Pelt.colour_categories, k=1)[0])

        # ------------------------------------------------------------------------------------------------------------#
        #   PELT LENGTH
        # ------------------------------------------------------------------------------------------------------------#

        chosen_pelt_length = random.choice(Pelt.pelt_length)

        # ------------------------------------------------------------------------------------------------------------#
        #   PELT WHITE
        # ------------------------------------------------------------------------------------------------------------#

        chosen_white = random.randint(1, 100) <= 40

        # Adjustments to pelt chosen based on if the pelt has white in it or not.
        if chosen_pelt in ("TwoColour", "SingleColour"):
            if chosen_white:
                chosen_pelt = "TwoColour"
            else:
                chosen_pelt = "SingleColour"
        elif chosen_pelt == "Calico":
            if not chosen_white:
                chosen_pelt = "Tortie"

        self.name = chosen_pelt
        self.colour = chosen_pelt_color
        self.length = chosen_pelt_length
        self.tortie_base = (
            chosen_tortie_base  # This will be none if the cat isn't a tortie.
        )
        return chosen_white

    def init_pattern_color(self, parents, gender) -> bool:
        """Initializes self.name, self.colour, self.length,
        self.tortie_base and determines if the cat
        will have white patche or not.
        Return TRUE is the cat should have white patches,
        false is not."""

        if parents:
            # If the cat has parents, use inheritance to decide pelt.
            chosen_white = self.pattern_color_inheritance(parents, gender)
        else:
            chosen_white = self.randomize_pattern_color(gender)

        return chosen_white

    def init_sprite(self):
        self.cat_sprites = {
            "newborn": random.choice(self.newborn_poses),
            "kitten": random.choice(self.kitten_poses),
            "senior": random.choice(self.senior_poses),
            "para_young": "para_young0",
        }
        self.reverse = bool(random.getrandbits(1))
        # skin chances
        self.skin = choice(Pelt.skin_sprites)

        if self.length == "long":
            self.cat_sprites["adolescent"] = random.choice(
                self.adolescent_long_poses
                if self.adolescent_long_poses
                else self.adolescent_short_poses
            )
            self.cat_sprites["adult"] = random.choice(
                self.adult_long_poses
                if self.adult_long_poses
                else self.adult_short_poses
            )
            self.cat_sprites["para_adult"] = "para_adult_long0"
        else:
            self.cat_sprites["adolescent"] = random.choice(self.adolescent_short_poses)
            self.cat_sprites["adult"] = random.choice(self.adult_short_poses)
            self.cat_sprites["para_adult"] = "para_adult_short0"

        self.cat_sprites["young adult"] = self.cat_sprites["adult"]
        self.cat_sprites["senior adult"] = self.cat_sprites["adult"]

    def init_scars(self, age):
        if age == "newborn":
            return

        if age in ("kitten", "adolescent"):
            scar_choice = random.randint(0, 50)  # 2%
        elif age in ("young adult", "adult"):
            scar_choice = random.randint(0, 20)  # 5%
        else:
            scar_choice = random.randint(0, 15)  # 6.67%

        if scar_choice == 1:
            self.scars = (*self.scars, choice(Pelt.general_scars))

        if "NOTAIL" in self.scars and "HALFTAIL" in self.scars:
            self.scars = tuple(scar for scar in self.scars if scar != "HALFTAIL")

    def init_accessories(self, age):
        if age == "newborn":
            self.accessory = tuple()
            return

        acc_display_choice = random.randint(0, 80)
        if age in ("kitten", "adolescent"):
            acc_display_choice = random.randint(0, 180)
        elif age in ("young adult", "adult"):
            acc_display_choice = random.randint(0, 100)

        if acc_display_choice == 1:
            self.accessory = tuple(
                (choice(Pelt.plant_accessories + Pelt.wild_accessories),)
            )
        else:
            self.accessory = tuple()

    def init_pattern(self):
        if self.name in Pelt.torties:
            if not self.tortie_base:
                self.tortie_base = choice(Pelt.pelt_patterns)
            if not self.tortie_marking:
                self.tortie_marking = choice(Pelt.tortie_patches)

            wildcard_chance = constants.CONFIG["cat_generation"]["wildcard_tortie"]
            if self.colour:
                # The "not wildcard_chance" allows users to set wildcard_tortie to 0
                # and always get wildcard torties.
                if not wildcard_chance or random.getrandbits(wildcard_chance) == 1:
                    # This is the "wildcard" chance, where you can get funky combinations.
                    # people are fans of the print message, so I'm putting it back
                    print("Wildcard tortie!")

                    # Allow any pattern, minus tories:
                    self.tortie_pattern = choice(
                        self.exotic + self.tabbies + self.spotted + self.plain
                    )

                    # Allow any colors that aren't the base color.
                    possible_colors = Pelt.all_pelt_colours.copy()
                    possible_colors.remove(self.colour)
                    self.tortie_colour = choice(possible_colors)

                else:
                    # Normal generation
                    if self.tortie_base in ("SingleStripe", "Smoke"):
                        self.tortie_pattern = choice(
                            [
                                "Tabby",
                                "Mackerel",
                                "Classic",
                                "SingleColour",
                                "Smoke",
                                "Agouti",
                                "Ticked",
                            ]
                        )
                    else:
                        self.tortie_pattern = random.choices(
                            [self.tortie_base, "SingleColour"], weights=[97, 3], k=1
                        )[0]

                    if self.colour == "WHITE":
                        possible_colors = Pelt.white_colours.copy()
                        possible_colors.remove("WHITE")
                        self.colour = choice(possible_colors)

                    # Ginger is often duplicated to increase its chances
                    if (self.colour in Pelt.black_colours) or (
                        self.colour in Pelt.white_colours
                    ):
                        self.tortie_colour = choice(
                            (Pelt.ginger_colours * 2) + Pelt.brown_colours
                        )
                    elif self.colour in Pelt.ginger_colours:
                        self.tortie_colour = choice(
                            Pelt.brown_colours + Pelt.black_colours * 2
                        )
                    elif self.colour in Pelt.brown_colours:
                        possible_colors = Pelt.brown_colours.copy()
                        possible_colors.remove(self.colour)
                        possible_colors.extend(
                            Pelt.black_colours + (Pelt.ginger_colours * 2)
                        )
                        self.tortie_colour = choice(possible_colors)
                    else:
                        self.tortie_colour = "GOLDEN"

            else:
                self.tortie_colour = "GOLDEN"
        else:
            self.tortie_base = None
            self.tortie_pattern = None
            self.tortie_colour = None
            self.tortie_marking = None

    def white_patches_inheritance(self, parents: tuple):
        par_whitepatches = set()
        par_points = []
        for p in parents:
            if p:
                if p.pelt.white_patches:
                    par_whitepatches.add(p.pelt.white_patches)
                if p.pelt.points:
                    par_points.append(p.pelt.points)

        if not parents:
            print("Error - no parents. Randomizing white patches.")
            self.randomize_white_patches()
            return

        # Direct inheritance. Will only work if at least one parent has white patches, otherwise continue on.
        if par_whitepatches and not random.randint(
            0, constants.CONFIG["cat_generation"]["direct_inheritance"]
        ):
            # This ensures Torties and Calicos won't get direct inheritance of incorrect white patch types
            _temp = par_whitepatches.copy()
            if self.name == "Tortie":
                for p in _temp.copy():
                    if p in Pelt.high_white + Pelt.mostly_white + ["FULLWHITE"]:
                        _temp.remove(p)
            elif self.name == "Calico":
                for p in _temp.copy():
                    if p in Pelt.little_white + Pelt.mid_white:
                        _temp.remove(p)

            # Only proceed with the direct inheritance if there are white patches that match the pelt.
            if _temp:
                self.white_patches = choice(list(_temp))

                # Direct inheritance also effect the point marking.
                if par_points and self.name != "Tortie":
                    self.points = choice(par_points)
                else:
                    self.points = None

                return

        # dealing with points
        if par_points:
            chance = 10 - len(par_points)
        else:
            chance = 40
        # Chance of point is 1 / chance.
        if self.name != "Tortie" and not int(random.random() * chance):
            self.points = choice(Pelt.point_markings)
        else:
            self.points = None

        white_list = [
            Pelt.little_white,
            Pelt.mid_white,
            Pelt.high_white,
            Pelt.mostly_white,
            ["FULLWHITE"],
        ]

        weights = [0, 0, 0, 0, 0]  # Same order as white_list
        for p_ in par_whitepatches:
            if p_ in Pelt.little_white:
                add_weights = (40, 20, 15, 5, 0)
            elif p_ in Pelt.mid_white:
                add_weights = (10, 40, 15, 10, 0)
            elif p_ in Pelt.high_white:
                add_weights = (15, 20, 40, 10, 1)
            elif p_ in Pelt.mostly_white:
                add_weights = (5, 15, 20, 40, 5)
            elif p_ == "FULLWHITE":
                add_weights = (0, 5, 15, 40, 10)
            else:
                add_weights = (0, 0, 0, 0, 0)

            for x in range(0, len(weights)):
                weights[x] += add_weights[x]

        # If all the weights are still 0, that means none of the parents have white patches.
        if not any(weights):
            if not all(
                parents
            ):  # If any of the parents are None (unknown), use the following distribution:
                weights = [20, 10, 10, 5, 0]
            else:
                # Otherwise, all parents are known and don't have any white patches. Focus distribution on little_white.
                weights = [50, 5, 0, 0, 0]

        # Adjust weights for torties, since they can't have anything greater than mid_white:
        if self.name == "Tortie":
            weights = weights[:2] + [0, 0, 0]
            # Another check to make sure not all the values are zero. This should never happen, but better
            # safe than sorry.
            if not any(weights):
                weights = [2, 1, 0, 0, 0]
        elif self.name == "Calico":
            weights = [0, 0, 0] + weights[3:]
            # Another check to make sure not all the values are zero. This should never happen, but better
            # safe than sorry.
            if not any(weights):
                weights = [2, 1, 0, 0, 0]

        chosen_white_patches = choice(
            random.choices(white_list, weights=weights, k=1)[0]
        )

        self.white_patches = chosen_white_patches
        if self.points and self.white_patches in (
            Pelt.high_white,
            Pelt.mostly_white,
            "FULLWHITE",
        ):
            self.points = None

    def randomize_white_patches(self):
        # Points determination. Tortie can't be pointed
        if self.name != "Tortie" and not random.getrandbits(
            constants.CONFIG["cat_generation"]["random_point_chance"]
        ):
            # Cat has colorpoint!
            self.points = choice(Pelt.point_markings)
        else:
            self.points = None

        # Adjust weights for torties, since they can't have anything greater than mid_white:
        if self.name == "Tortie":
            weights = (2, 1, 0, 0, 0)
        elif self.name == "Calico":
            weights = (0, 0, 20, 15, 1)
        else:
            weights = (10, 10, 10, 10, 1)

        white_list = [
            Pelt.little_white,
            Pelt.mid_white,
            Pelt.high_white,
            Pelt.mostly_white,
            ["FULLWHITE"],
        ]
        chosen_white_patches = choice(
            random.choices(white_list, weights=weights, k=1)[0]
        )

        self.white_patches = chosen_white_patches
        if self.points and self.white_patches in (
            Pelt.high_white,
            Pelt.mostly_white,
            "FULLWHITE",
        ):
            self.points = None

    def init_white_patches(self, pelt_white, parents: tuple):
        # Vit can roll for anyone, not just cats who rolled to have white in their pelt.
        par_vit = []
        for p in parents:
            if p:
                if p.pelt.vitiligo:
                    par_vit.append(p.pelt.vitiligo)

        vit_chance = max(
            constants.CONFIG["cat_generation"]["vit_chance"] - len(par_vit), 0
        )
        if not random.getrandbits(vit_chance):
            self.vitiligo = choice(Pelt.vitiligo_markings)

        # If the cat was rolled previously to have white patches, then determine the patch they will have
        # these functions also handle points.
        if pelt_white:
            if parents:
                self.white_patches_inheritance(parents)
            else:
                self.randomize_white_patches()
        else:
            self.white_patches = None
            self.points = None

    def init_tint(self):
        """Sets tint for pelt and white patches"""
        # PELT TINT
        # Basic tints as possible for all colors.
        base_tints = sprites.cat_tints["possible_tints"]["basic"]
        if self.colour in sprites.cat_tints["colour_groups"]:
            color_group = sprites.cat_tints["colour_groups"].get(self.colour, "warm")
            color_tints = sprites.cat_tints["possible_tints"][color_group]
        else:
            color_tints = []

        if base_tints or color_tints:
            self.tint = choice(base_tints + color_tints)
        else:
            self.tint = None

        # WHITE PATCHES TINT
        if self.white_patches or self.points:
            # Now for white patches
            base_tints = sprites.white_patches_tints["possible_tints"]["basic"]
            if self.colour in sprites.cat_tints["colour_groups"]:
                color_group = sprites.white_patches_tints["colour_groups"].get(
                    self.colour, "white"
                )
                color_tints = sprites.white_patches_tints["possible_tints"][color_group]
            else:
                color_tints = []

            if base_tints or color_tints:
                self.white_patches_tint = choice(base_tints + color_tints)
            else:
                self.white_patches_tint = None
        else:
            self.white_patches_tint = None

    @property
    def white(self):
        return self.white_patches or self.points

    @white.setter
    def white(self, val):
        raise Exception(
            f"Attempted to set cat's white patches to {val}, but pelt.white cannot be used to set a white patches"
        )

    def describe_eyes(self):
        return (
            adjust_list_text(
                [
                    i18n.t(f"cat.eyes.{self.eye_colour}"),
                    i18n.t(f"cat.eyes.{self.eye_colour2}"),
                ]
            )
            if self.eye_colour2
            else i18n.t(f"cat.eyes.{self.eye_colour}")
        )

    @staticmethod
    def describe_appearance(cat, short=False):
        """Return a description of a cat

        :param Cat cat: The cat to describe
        :param bool short: Whether to return a heavily-truncated description, default False
        :return str: The cat's description
        """
        short=False # Modded: cats will always have colors in their descriptions
        
        config = get_lang_config()["description"]
        ruleset = config["ruleset"]
        output = []
        pelt_pattern, pelt_color = _describe_pattern(cat, short)
        for rule, args in ruleset.items():
            temp = unpack_appearance_ruleset(cat, rule, short, pelt_pattern, pelt_color)

            if args == "" or temp == "":
                output.append(temp)
                continue

            # handle args
            arg_pool = {
                arg: unpack_appearance_ruleset(
                    cat, arg, short, pelt_pattern, pelt_color
                )
                for arg in args
            }
            arg_pool["key"] = temp
            arg_pool["count"] = 1 if short else 2
            output.append(i18n.t(**arg_pool))

        # don't forget the count argument!
        groups = []
        for grouping in config["groups"]:
            temp = ""
            items = [
                i18n.t(output[i], count=1 if short else 2)
                for i in grouping["values"]
                if output[i] != ""
            ]
            if len(items) == 0:
                continue
            if "pre_value" in grouping:
                temp = grouping["pre_value"]

            if grouping["format"] == "list":
                temp += adjust_list_text(items)
            else:
                temp += grouping["format"].join(items)

            if "post_value" in grouping:
                temp += grouping["post_value"]
            groups.append(temp)

        return "".join(groups)

    """
    def get_sprites_name(self):
        return Pelt.pattern_sprite_names[self.name]
    """


def _describe_pattern(cat, short=False):
    #Modded: description color now does tints
    
    if cat.pelt.name in ["Tortie", "Calico"]:
        pelt_name = "cat.pelts.mottled_long"
    else:
        pelt_name = f"cat.pelts.{cat.pelt.name}{'' if short else '_long'}"
    
    # Create list of HSV colors, so an do for loop for color namer
    color_list = [colorsys.rgb_to_hsv(cat.pelt.tint[0]/255, cat.pelt.tint[1]/255, cat.pelt.tint[2]/255)]
    if cat.pelt.white_patches_tint != None:
        color_list.append(colorsys.rgb_to_hsv(cat.pelt.white_patches_tint[0]/255, cat.pelt.white_patches_tint[1]/255, cat.pelt.white_patches_tint[2]/255))
    
    color_name = '' #text describing cat's color
    
    hue = 'none' 
    
    
    
    for color in color_list:
        
        #Hue setup
        hue = ''
        
        hue_desc = {
            0: "red",
            0.04: "orange",
            0.12: "yellow",
            0.18: "lime",
            0.27: "green",
            0.40: "mint",
            0.45: "cyan",
            0.55: "blue",
            0.67: "indigo",
            0.75: "purple",
            0.79: "magenta",
            0.96: "red"
            }

        for hue_val in hue_desc:
            if color[0] >= hue_val:
                hue = hue_desc[hue_val]
        
        
        # Saturation/Value descriptor charts
        
        # Saturation cutoff values. Make sure list starts at 1, # of values matches # of entries in color_desc lists
        saturation_list = [1, 0.9, 0.8, 0.5, 0.2, 0.1]
        
        color_desc = {
#Value:         bright           saturated          comfy              faded            dull              desaturated
        1    : [f'neon {hue}',   f'bright {hue}',   f'glowing {hue}',  f'pastel {hue}',  f'pale {hue}',   'white'],
        0.85 : [f'vivid {hue}',  f'vibrant {hue}',  f'soft {hue}',     f'faded {hue}',   f'dull {hue}',   'pale gray'],
        0.75 : [f'deep {hue}',   f'cloudy {hue}',   f'dim {hue}',      f'grayed-{hue}',  f'drab {hue}',   'light gray'],
        0.5  : [f'rich {hue}',   f'dusky {hue}',    f'dark {hue}',     f'murky {hue}',   f'{hue}-gray',   'gray'],
        0.3  : [f'black-{hue}',  f'oil-{hue}',      f'inky {hue}',     f'shadow-{hue}',  f'sooty {hue}',  'dark gray'],           
        0.1  : ['black']*6          #Black
                
                }
        
        # Modifier setup
        
        modifier = 'ERROR'
            
        for saturation in saturation_list:
            if color[1] <= saturation:
                sat = saturation_list.index(saturation)
        
        for value in color_desc:
            if color[2] <= value:
                modifier = color_desc[value][sat]
        
        
        color_name = color_name + modifier  + '/'
        
        #print(f' color:{color} desc:{modifier}')
    
    color_name = color_name[:-1]
    

    return pelt_name, color_name




def _describe_torties(cat, color_name, short=False) -> (str, str):
    # Calicos and Torties need their own descriptions
    if short:
        # If using short, don't describe the colors of calicos and torties.
        # Just call them calico, tortie, or mottled
        if (
            cat.pelt.colour
            in Pelt.black_colours + Pelt.brown_colours + Pelt.white_colours
            and cat.pelt.tortie_colour
            in Pelt.black_colours + Pelt.brown_colours + Pelt.white_colours
        ):
            return "cat.pelts.mottled", ""
        else:
            return f"cat.pelts.{cat.pelt.name}", ""

    base = cat.pelt.tortie_base.lower()

    patches_color = f"cat.pelts.{cat.pelt.tortie_colour}"
    color_name.append("/")
    color_name.append(patches_color)

    if (
        cat.pelt.colour in Pelt.black_colours + Pelt.brown_colours + Pelt.white_colours
        and cat.pelt.tortie_colour
        in Pelt.black_colours + Pelt.brown_colours + Pelt.white_colours
    ):
        return "cat.pelts.mottled_long", color_name
    else:
        if base in tuple(tabby.lower() for tabby in Pelt.tabbies) + (
            "bengal",
            "rosette",
            "speckled",
        ):
            base = f"cat.pelts.{cat.pelt.name}_tabby_long"
        else:
            base = f"cat.pelts.{cat.pelt.name}_long"
        return base, color_name


_scar_details = [
    "NOTAIL",
    "HALFTAIL",
    "NOPAW",
    "NOLEFTEAR",
    "NORIGHTEAR",
    "NOEAR",
]


def unpack_appearance_ruleset(cat, rule, short, pelt, color):
    if rule == "scarred":
        if not short and len(cat.pelt.scars) >= 3:
            return "cat.pelts.scarred"
    elif rule == "fur_length":
        if not short and cat.pelt.length == "long":
            return "cat.pelts.long_furred"
    elif rule == "pattern":
        return pelt
    elif rule == "color":
        return color
    elif rule == "cat":
        if cat.genderalign in ("female", "trans female"):
            return "general.she-cat"
        elif cat.genderalign in ("male", "trans male"):
            return "general.tom"
        else:
            return "general.cat"
    elif rule == "vitiligo":
        if not short and cat.pelt.vitiligo:
            return "cat.pelts.vitiligo"
    elif rule == "amputation":
        if not short:
            scarlist = []
            for scar in cat.pelt.scars:
                if scar in _scar_details:
                    scarlist.append(i18n.t(f"cat.pelts.{scar}"))
            return (
                adjust_list_text(list(set(scarlist))) if len(scarlist) > 0 else ""
            )  # note: this doesn't preserve order!
    else:
        raise Exception(f"Unmatched ruleset item {rule} in describe_appearance!")
    return ""

