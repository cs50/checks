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
            raise Error("More than one .sb3 file found. Make sure there's only one!")
        elif len(filenames) == 0:
            raise Error("No .sb3 file found.")
        filename = filenames[0]

        # Ensure that unzipped .sb2 file contains .json file.
        if self.spawn("unzip {}".format(shlex.quote(filename))).exit():
            raise Error("Invalid .sb3 file.")
        self.require("project.json")

    @check("valid")
    def two_sprites(self):
        """project contains at least two sprites"""
        project = json.loads(File("project.json").read())["targets"]
        num_sprites = sum(not target["isStage"] for target in project)
        if num_sprites < 2:
            raise Error(f"Only {num_sprites} sprite{'' if num_sprites == 1 else 's'} found, 2 required.")

    @check("valid")
    def non_cat(self):
        """project contains a non-cat sprite"""
        project = json.loads(File("project.json").read())["targets"]

        cat_sprite_ids = {"fc0687f38ae230b8765eebf4100e2653", "06c57b43f5a7d3500fd149de265c2289"}
        if all(target["isStage"] or {costume["assetId"] for costume in target["costumes"]} == cat_sprite_ids for target in project):
            raise Error("Requires a non-cat sprite.")

    @check("valid")
    def three_scripts(self):
        """project contains at least three scripts"""
        project = json.loads(File("project.json").read())["targets"]
        num_scripts = sum(len(target["blocks"]) for target in project)
        if num_scripts < 3:
            raise Error(f"Only {num_scripts} script{'' if num_scripts == 1 else 's'} found, 3 required.")

    @check("valid")
    def uses_condition(self):
        """project uses at least one condition"""
        project = json.loads(File("project.json").read())["targets"]
        if not contains_blocks(project, ["control_repeat", "control_if_else", "control_if"]):
            raise Error("No conditions found, 1 required.")

    @check("valid")
    def uses_loop(self):
        """project uses at least one loop"""
        project = json.loads(File("project.json").read())["targets"]
        if not contains_blocks(project, ["control_forever", "control_repeat_until", "control_repeat"]):
            raise Error("No loops found, 1 required.")

    @check("valid")
    def uses_variable(self):
        """project uses at least one variable"""
        project = json.loads(File("project.json").read())["targets"]
        if not any(target["variables"] for target in project):
            raise Error("No variables found, 1 required.")

    @check("valid")
    def uses_sound(self):
        """project uses at least one sound"""
        project = json.loads(File("project.json").read())["targets"]
        if not contains_blocks(project, ["sound_play", "sound_playuntildone"]):
            raise Error("No sounds used, 1 required")

def contains_blocks(project, opcodes):
    """Return whether project contains any blocks with their names in opcodes"""
    return any(any(block["opcode"] in opcodes for block in target["blocks"].values()) for target in project)
