"""
Module that handles the name generation for all cats.
"""

import contextlib
import os
import random
import colorsys #modded: allows hsv

import i18n
import ujson

from scripts.game_structure import constants
from scripts.cat.enums import CatRank, CatGroup, CatAge, CatSocial
from scripts.game_structure.localization import load_lang_resource
from scripts.housekeeping.datadir import get_save_dir


class Name:
    """
    Stores & handles name generation.
    """

    current_save_dir = None
    currently_loaded_lang = None
    names_dict = {}
    prefix_history = []

    def __init__(
        self,
        prefix=None,
        suffix=None,
        biome=None,
        specsuffix_hidden=False,
        load_existing_name=False,
        cat=None,
    ):
        self.load_localized_names()
        self.prefix = prefix
        self.suffix = suffix
        self.specsuffix_hidden = specsuffix_hidden

        self.cat = cat

#Modded: define color lists
        hue_desc = {
            0: "Red",
            0.04: "Orange",
            0.12: "Yellow",
            0.18: "Lime",
            0.27: "Green",
            0.40: "Mint",
            0.45: "Cyan",
            0.55: "Blue",
            0.67: "Indigo",
            0.75: "Purple",
            0.79: "Magenta",
            0.96: "Red"
            }

        saturation_list = [1, 0.5, 0.1]
        
        color_desc = {

        1    : [f'Bright',     f'Pale',    'Desat'],
        0.75 : [f'Dusky',      f'Drab',    'Desat'],
        0.3  : [f'Inky',       f'Shadow',  'Desat'],           
        0.1  : ['Desat']*3          #Black
                
                }
        desat_list = {
            1: "White",
            0.85: "PaleGray",
            0.75: "LightGray",
            0.5: "Gray",
            0.3: "DarkGray",
            0.1: "Black"
            }



        try:
            
            #Modded: replace color with tint name
            #print(cat.pelt.tint)
            
            color_hsv = colorsys.rgb_to_hsv(cat.pelt.tint[0]/255, cat.pelt.tint[1]/255, cat.pelt.tint[2]/255)
            for hue_val in hue_desc:
                if color_hsv[0] >= hue_val:
                    hue = hue_desc[hue_val]
                    
            modifier = 'ERROR'
            
            for saturation in saturation_list:
                if color_hsv[1] <= saturation:
                    sat = saturation_list.index(saturation)
            
            for value in color_desc:
                if color_hsv[2] <= value:
                    modifier = color_desc[value][sat]
            
            #Handle desaturated!=
            if modifier == "Desat":
                for value in desat_list:
                    if color_hsv[2] <= value:
                        color = [desat_list[value], None]
                
            else:
                color =  [modifier+hue, None]
            #print(f"{color}  {color_hsv}")
            
            if cat.pelt.white_patches:
                color[1] = "multi"
            
            
            eyes = cat.pelt.eye_colour
            pelt = cat.pelt.name
            tortie_pattern = cat.pelt.tortie_pattern
        except AttributeError:
            color = [None, None]
            eyes = None
            pelt = None
            tortie_pattern = None
            
            
            
        prefix_type = "other_categories"
        name_fixpref = False
        # Set prefix
        if prefix is None:
            prefix_type = self.give_prefix(eyes, color, pelt, biome)
            # needed for random dice when we're changing the Prefix
            name_fixpref = True

        # Set suffix
        if self.suffix is None:
            self.give_suffix(eyes, color, pelt, biome, tortie_pattern, prefix_type) #pass prefix type if initial name generation)
            if name_fixpref and self.prefix is None:
                # needed for random dice when we're changing the Prefix
                name_fixpref = False

        if self.suffix and not load_existing_name:
            # check if random die was for prefix
            if name_fixpref:
                self.give_prefix(eyes, color, pelt, biome)
            else:
                self.give_suffix(eyes, color, pelt, biome, tortie_pattern)

    @classmethod
    def _usable_name(cls, prefix, suffix):
        if prefix is None or suffix is None:
            return True

        name = prefix + suffix

        # Prevent triple letter names from joining prefix and suffix from occurring (ex. Beeeye)
        # Prevent crash on empty prefix or suffix (e.g. empty-suffix loner names)
        if not prefix or not suffix:
            triple_letter = False
        else:
            possible_three_letter = (
                prefix[-2:] + suffix[0],
                prefix[-1] + suffix[:2],
            )
            triple_letter = all(
                i == possible_three_letter[0][0] for i in possible_three_letter[0]
            ) or all(i == possible_three_letter[1][0] for i in possible_three_letter[1])

        # Prevent double animal names (ex. Spiderfalcon)
        double_animal = (
            prefix in cls.names_dict["animal_prefixes"]
            and suffix in cls.names_dict["animal_suffixes"]
        )

        # Prevent double names (ex. Iceice)
        # Prevent suffixes containing the prefix (ex. Butterflyfly)
        double_name = (prefix.lower() in suffix.lower() and str(prefix) != "") or (
            suffix.lower() in prefix.lower() and str(suffix) != ""
        )

        return not (
            # Prevent the inappropriate names
            name.lower() in cls.names_dict["inappropriate_names"]
            or triple_letter
            or double_animal
            or double_name
        )

    @classmethod
    def load_localized_names(cls):
        """
        Loads the correct names for the given language. Includes override for always using English names, in case localization wants to be ignored
        :return: None
        """

        # allowing the user to override the localized language names if desired
        if always_english := constants.CONFIG["cat_name_controls"][
            "always_use_english"
        ]:
            lang = "en"
        else:
            lang = i18n.config.get("locale")

        if cls.current_save_dir == get_save_dir() and cls.currently_loaded_lang == lang:
            # nothing to do here, all good
            return

        if always_english:
            with open("resources/lang/en/names.json", encoding="utf-8") as read_file:
                names_dict = ujson.loads(read_file.read())
        else:
            names_dict = load_lang_resource("names.json")

        save_dir = get_save_dir()

        # here onwards is copied wholesale from the original Name class

        if os.path.exists(save_dir + "/prefixlist.txt"):
            with open(
                str(save_dir + "/prefixlist.txt"), "r", encoding="utf-8"
            ) as read_file:
                name_list = read_file.read()
                if_names = len(name_list)
            if if_names > 0:
                new_names = name_list.split("\n")
                for new_name in new_names:
                    if new_name != "":
                        if new_name.startswith("-"):
                            while new_name[1:] in names_dict["normal_prefixes"]:
                                names_dict["normal_prefixes"].remove(new_name[1:])
                        else:
                            names_dict["normal_prefixes"].append(new_name)

        if os.path.exists(save_dir + "/suffixlist.txt"):
            with open(
                str(save_dir + "/suffixlist.txt"), "r", encoding="utf-8"
            ) as read_file:
                name_list = read_file.read()
                if_names = len(name_list)
            if if_names > 0:
                new_names = name_list.split("\n")
                for new_name in new_names:
                    if new_name != "":
                        if new_name.startswith("-"):
                            while new_name[1:] in names_dict["normal_suffixes"]:
                                names_dict["normal_suffixes"].remove(new_name[1:])
                        else:
                            names_dict["normal_suffixes"].append(new_name)

        if os.path.exists(save_dir + "/specialsuffixes.txt"):
            with open(
                str(save_dir + "/specialsuffixes.txt", "r"), encoding="utf-8"
            ) as read_file:
                name_list = read_file.read()
                if_names = len(name_list)
            if len(name_list) > 0:
                new_names = name_list.split("\n")
                for new_name in new_names:
                    if new_name != "":
                        if new_name.startswith("-"):
                            del names_dict["special_suffixes"][new_name[1:]]
                        elif ":" in new_name:
                            _tmp = new_name.split(":")
                            names_dict["special_suffixes"][_tmp[0]] = _tmp[1]

        cls.names_dict = names_dict
        cls.current_save_dir = save_dir
        cls.currently_loaded_lang = lang

    def __str__(self):
        return self.__repr__()

    def find_outsider_name(self, social: CatSocial):
        if social == CatSocial.CLANCAT:
            return

        # if it ain't a clancat, give it a non-clancat name
        name_categories = [
            "silly_names",
            "human_names",
            "loner_names",
            "normal_prefixes",
        ]
        # defaults in case of error
        weights = [1, 1, 1, 1]
        # give kittypets a kittypet name
        weights = constants.CONFIG["cat_name_controls"][str(social)]

        selected_category = random.choices(name_categories, weights, k=1)[0]
        name = random.choice(self.names_dict[selected_category])
        self.cat.change_name(new_prefix=name, new_suffix="")

    # Generate possible prefix
    def give_prefix(self, eyes, colour, pelt, biome):
        """Generate possible prefix."""
        self.load_localized_names()

        # Add possible prefix categories to list.
        possible_prefix_categories = {
            "eye_categories" : [],
            "fur_categories": [],
            "biome_categories": [],
            "other_categories": [self.names_dict["normal_prefixes"]]
            }
      
        if (
            eyes in self.names_dict["eye_prefixes"]
            and constants.CONFIG["cat_name_controls"]["allow_eye_names"]
        ):
            possible_prefix_categories["eye_categories"].append(self.names_dict["eye_prefixes"][eyes])
        
        if colour[0] in self.names_dict["colour_prefixes"]:
            possible_prefix_categories["fur_categories"].append(self.names_dict["colour_prefixes"][colour[0]])

        if colour[1] == "multi":
            possible_prefix_categories["fur_categories"].append(self.names_dict["colour_prefixes"]["Multicolor"])
                
        if pelt in self.names_dict["pelt_prefixes"]:
            possible_prefix_categories["fur_categories"].append(self.names_dict["pelt_prefixes"][pelt])
            
        if biome is not None and biome in self.names_dict["biome_prefixes"]:
            possible_prefix_categories["biome_categories"].append(self.names_dict["biome_prefixes"][biome])

        while True:
            # decided in constants.CONFIG: cat_name_controls
            if constants.CONFIG["cat_name_controls"]["always_name_after_appearance"]:
                named_after_appearance = True
            else:
                named_after_appearance = not random.getrandbits(1)  # Chance for True is 1/2
            
            named_after_biome = not random.getrandbits(3)  # chance for True is 1/8 
            
            if named_after_appearance:
                prefix_category = random.choices(["eye_categories", "fur_categories"], weights = (1, 10))[0]
            elif named_after_biome:
               prefix_category = "biome_categories"
            else:
                prefix_category = "other_categories"
            
            # If chosen category is empty, set chosen category to normal
            if possible_prefix_categories[prefix_category] == []:
                prefix_category = "other_categories"
            
            self.prefix = random.choice(random.choice(possible_prefix_categories[prefix_category]))
            
            # prevent prefix duplications from happening
            if self.prefix in self.prefix_history or not self._usable_name(
                self.prefix, self.suffix
            ):
                continue
            else:
                self.prefix_history.append(self.prefix)
                # Set the maximin length to 8 just to be sure
                if len(self.prefix_history) > 20:
                    # removing at zero so the oldest gets removed
                    self.prefix_history.pop(0)
                print(prefix_category)
                return prefix_category

    # Generate possible suffix
    def give_suffix(self, eyes, colour, pelt, biome, tortie_pattern, prefix_type = "other_categories"):
        """Generate possible suffix."""
        self.load_localized_names()
        
        
        possible_suffix_categories = {
            "eye_desc_categories" : [self.names_dict["eye_desc_suffixes"]], #!!! change
            "fur_desc_categories": [self.names_dict["pelt_desc_suffixes"]], #!!! change
            
            "eye_categories" : [],
            "fur_categories": [],
            "biome_categories": [],
            "other_categories": [self.names_dict["normal_suffixes"]]
            }
  
        if (constants.CONFIG["cat_name_controls"]["allow_eye_names"] and eyes in self.names_dict["eye_suffixes"]):
            possible_suffix_categories["eye_categories"].append(self.names_dict["eye_suffixes"][eyes])
            
        if (colour[0] in self.names_dict["colour_suffixes"]):
            possible_suffix_categories["fur_categories"].append(self.names_dict["colour_suffixes"][colour[0]])
        
        if colour[1] == "multi":
            possible_suffix_categories["fur_categories"].append(self.names_dict["colour_suffixes"]["Multicolor"])
         
            
        if (pelt in self.names_dict["pelt_suffixes"]):
            possible_suffix_categories["fur_categories"].append(self.names_dict["pelt_suffixes"][pelt])
            
        if (pelt in ("Tortie", "Calico") and tortie_pattern in self.names_dict["tortie_pelt_suffixes"]):
            possible_suffix_categories["fur_categories"].append(self.names_dict["tortie_pelt_suffixes"][tortie_pattern])
            
        if biome in self.names_dict["biome_suffixes"]:
            possible_suffix_categories["biome_categories"].append(self.names_dict["biome_suffixes"][biome])


        # If prefix describes fur color/pattern, limit suffixes to non-appearance and fur desc
        if prefix_type == "fur_categories":
            possible_suffix_categories["eye_categories"] = []
            possible_suffix_categories["fur_categories"] = []
            possible_suffix_categories["eye_desc_categories"] = []
        
        # If prefix describes eye color, limit suffixes to non-appearance and eye desc
        if prefix_type == "eye_categories":
            possible_suffix_categories["eye_categories"] = []
            possible_suffix_categories["fur_categories"] = []
            possible_suffix_categories["fur_desc_categories"] = []
        
        while True:
            if pelt is not None or pelt != "SingleColour":
                named_after_pelt = not random.getrandbits(2)  # Chance for True is '1/4'.
            else:
                named_after_pelt = false
                
            named_after_biome = not random.getrandbits(3)  # 1/8
               
               
            if named_after_pelt:
                suffix_category = random.choices(["eye_categories", "fur_categories", "eye_desc_categories", "fur_desc_categories"], weights = (2, 5, 1, 2))[0]
            elif named_after_biome:
               suffix_category = "biome_categories"
            else:
                suffix_category = random.choices(["other_categories", "eye_desc_categories", "fur_desc_categories"], weights = (10, 1, 2))[0]
            
            # If chosen category is empty, set chosen category to normal
            if possible_suffix_categories[suffix_category] == []:
                suffix_category = "other_categories"
                
            self.suffix = random.choice(random.choice(possible_suffix_categories[suffix_category]))
            
            if self._usable_name(self.prefix, self.suffix):
                return


    def get_specsuffix_name(self, rank: CatRank = CatRank.LEADER):
        """
        Return the cat's name with the appropriate special suffix. If no specsuffix is given for that rank, returns
        default prefix + suffix. If specsuffix_hidden is true, return default prefix + suffix.
        :param rank: CatRank matching
        :return: Cat's name string
        """
        self.load_localized_names()

        if rank in self.names_dict["special_suffixes"] and not self.specsuffix_hidden:
            return self.prefix + self.names_dict["special_suffixes"][rank]

        return self.prefix + self.suffix

    def __repr__(self):
        # Handles predefined suffixes (such as newborns being kit),
        # then suffixes based on ages (fixes #2004, just trust me)
        self.load_localized_names()

        # Handles suffix assignment with outside cats
        if (
            self.cat.status.is_lost(CatGroup.PLAYER_CLAN_ID)
            and not self.cat.status.is_former_clancat
            and self.suffix
        ):
            # these are cats who were born to a parent who'd been lost frm their clan, and who's parent decided to keep with traditional naming
            age_to_rank = {
                CatAge.NEWBORN: CatRank.NEWBORN,
                CatAge.KITTEN: CatRank.KITTEN,
                CatAge.ADOLESCENT: CatRank.APPRENTICE,
            }
            if self.cat.age in age_to_rank:
                rank = age_to_rank[self.cat.age]
                return self.prefix + self.names_dict["special_suffixes"][rank]
            else:
                return self.prefix + self.suffix

        if self.cat.status.is_former_clancat:
            old_rank = self.cat.status.find_prior_clan_rank()

            if (
                old_rank in self.names_dict["special_suffixes"]
                and not self.specsuffix_hidden
            ):
                return self.prefix + self.names_dict["special_suffixes"][old_rank]

        if (
            self.cat.status.rank in self.names_dict["special_suffixes"]
            and not self.specsuffix_hidden
        ):
            return (
                self.prefix + self.names_dict["special_suffixes"][self.cat.status.rank]
            )
        if constants.CONFIG["fun"]["april_fools"]:
            return f"{self.prefix}egg"
        return self.prefix + self.suffix


Name.load_localized_names()
