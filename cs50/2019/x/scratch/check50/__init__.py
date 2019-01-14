import json
import os
import shlex

from check50 import *


class Scratch(Checks):

    @check()
    def valid(self):
        """project exists and is valid Scratch program"""

        # Make sure there is only one .sb3 file.
        filenames = [filename for filename in os.listdir() if filename.endswith(".sb3")]
        if len(filenames) > 1:
            filenames = [max(filenames, key=os.path.getmtime)]
        elif len(filenames) == 0:
            filenames = [filename for filename in os.listdir() if filename.endswith(".sb2")]
            if len(filenames) > 1:
                filenames = [max(filenames, key=os.path.getmtime)]
            elif len(filenames) == 0:
                raise Error("No .sb3 file found.")
        filename = filenames[0]

        # Ensure that unzipped .sb2 or .sb3 file contains .json file.
        if self.spawn("unzip {}".format(shlex.quote(filename))).exit():
            raise Error("Invalid Scratch file.")
        self.require("project.json")

    @check("valid")
    def two_sprites(self):
        """project contains at least two sprites"""
        project = json.loads(File("project.json").read())
        if "targets" in project:
            project = project["targets"]
            num_sprites = sum(not target["isStage"] for target in project)
        else:
            num_sprites = sum("costumes" in child for child in project["children"])

        if num_sprites < 2:
            raise Error(f"Only {num_sprites} sprite{'' if num_sprites == 1 else 's'} found, 2 required.")

    @check("valid")
    def non_cat(self):
        """project contains a non-cat sprite"""
        project = json.loads(File("project.json").read())
        if "targets" in project:
            project = project["targets"]
            cat_sprite_ids = {"b7853f557e4426412e64bb3da6531a99", "e6ddc55a6ddd9cc9d84fe0b4c21e016f"}
            if all(target["isStage"] or {costume["assetId"] for costume in target["costumes"]} == cat_sprite_ids for target in project):
                raise Error("Requires a non-cat sprite.")
        else:
            for child in project["children"]:
                if "costumes" not in child:
                    continue
            is_cat = any(costume["baseLayerMD5"] == "09dc888b0b7df19f70d81588ae73420e.svg" for costume in child.get("costumes", []))
            if not is_cat:
                return
            raise Error("Requires a non-cat sprite.")

    @check("valid")
    def three_scripts(self):
        """project contains at least three scripts"""
        project = json.loads(File("project.json").read())
        if "targets" in project:
            project = project["targets"]
            num_scripts = sum(sum(
                (isinstance(target["blocks"][block], dict) and (target["blocks"][block]["parent"] is None))
                for block in target["blocks"]) for target in project)
        else:
            num_scripts = sum(len(child.get("scripts", [])) for child in project["children"])
            num_scripts += len(project.get("scripts", []))
        if num_scripts < 3:
            raise Error(f"Only {num_scripts} script{'' if num_scripts == 1 else 's'} found, 3 required.")

    @check("valid")
    def uses_condition(self):
        """project uses at least one condition"""
        project = json.loads(File("project.json").read())
        if "targets" in project:
            project = project["targets"]
            if not contains_blocks(project, ["control_repeat", "control_if_else", "control_if"]):
                raise Error("No conditions found, 1 required.")
        else:
            if not scratch2_contains_keywords(project, ["doIf", "doIfElse", "doUntil"]):
                raise Error("No conditions found, 1 required.")

    @check("valid")
    def uses_loop(self):
        """project uses at least one loop"""
        project = json.loads(File("project.json").read())
        if "targets" in project:
            project = project["targets"]
            if not contains_blocks(project, ["control_forever", "control_repeat_until", "control_repeat"]):
                raise Error("No loops found, 1 required.")
        else:
            if not scratch2_contains_keywords(project, ["doRepeat", "doUntil", "doForever"]):
                raise Error("No loops found, 1 required.")

    @check("valid")
    def uses_variable(self):
        """project uses at least one variable"""
        project = json.loads(File("project.json").read())
        if "targets" in project:
            project = project["targets"]
            if not contains_blocks(project, ["data_setvariableto", "data_changevariableby"]):
                raise Error("No variables found, 1 required.")
        else:
            if project.get("variables"):
                return
            if any(child.get("variables") for child in project["children"]):
                return
            raise Error("No variables found, 1 required.")

    @check("valid")
    def uses_sound(self):
        """project uses at least one sound"""
        project = json.loads(File("project.json").read())
        if "targets" in project:
            project = project["targets"]
            if not contains_blocks(project, ["sound_play", "sound_playuntildone"]):
                raise Error("No sounds used, 1 required")
        else:
            keywords = ["playSound:", "doPlaySoundAndWait", "playDrum", "noteOn:duration:elapsed:from:"]
            if not scratch2_contains_keywords(project, keywords):
                raise Error("No sounds found, 1 required.")

def contains_blocks(project, opcodes):
    """Return whether project contains any blocks with their names in opcodes"""
    return any(any((isinstance(block, dict) and (block["opcode"] in opcodes)) for block in target["blocks"].values()) for target in project)


def scratch2_contains_keywords(project, keywords):
    """Returns True if project contains at least one of the keywords."""
    for child in project["children"] + [project]:
        if any(scratch2_contains(script, keywords) for script in child.get("scripts", [])):
            return True
    return False

def scratch2_contains(script, keywords):
    """Performs DFS on the script to determine if keyword exists."""
    if type(script) != list or not script:
        return False
    if script[0] in keywords:
        return True
    return any(scratch2_contains(child, keywords) for child in script)
