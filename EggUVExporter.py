import bpy
import os, subprocess, sys, re

"""
run this script in blender >2.7
"""


class BatchUVExporter:
    def __init__(self):
        self.view_layer = bpy.context.view_layer
        self.mFilePath = None
        bpy.ops.object.select_all()
        bpy.ops.object.delete()  # Delete the default stuff
        pass

    def parseModel(self):
        selection = bpy.context.selected_objects
        bpy.ops.object.select_all(action='DESELECT')
        if self.mFilePath is None:
            return
        for obj in selection:
            self.obj = obj
            obj.select_set(True)
            self.view_layer.objects.active = obj
            self.extractUV()
            bpy.ops.object.delete()

    def extractUV(self):
        if not hasattr(bpy.context.object.data, 'uv_layers') or not bpy.context.object.data.uv_layers:
            print(self.obj.name + " does not have UV map, skipping")
        else:
            exportPath = os.path.join(self.mFilePath, "uvs")
            os.makedirs(exportPath, exist_ok=True)
            legal_node_name = self.obj.name.replace(":", "")
            exportPath = os.path.join(exportPath, f"UV_{os.path.splitext(self.mFileName)[0]}_{legal_node_name}")
            bpy.ops.uv.export_layout(filepath=exportPath, mode='PNG', opacity=0.45)
            bpy.ops.uv.export_layout(filepath=exportPath, mode='SVG', opacity=1)

    def addModel(self, modelFilePath, import_type):
        self.mFilePath = modelFilePath
        bpy.ops.import_scene.egg(filepath=self.mFilePath)  # maybe replace with glob
        if import_type == "egg":
            pass

    def addEggFiles(self, modelFilePath, models):
        self.mFilePath = modelFilePath
        file_list = list()
        for model in models:
            file_list.append(dict(name=os.path.basename(model)))
        bpy.ops.import_scene.egg(
            filepath=self.mFilePath,
            directory=self.mFilePath,
            files=file_list
        )

    def addEggFile(self, modelFilePath):
        self.mFilePath = os.path.dirname(modelFilePath)
        self.mFileName = os.path.basename(modelFilePath)
        file_list = [dict(name=self.mFileName)]
        bpy.ops.import_scene.egg(
            filepath=self.mFilePath,
            directory=self.mFilePath,
            files=file_list
        )


if __name__ == "__main__":
    uv = BatchUVExporter()
    
    target_dir = "path/to/eggfiles"

    os.chdir(
        target_dir
    )
    allFiles = []
    inputFile = ".egg"

    for root, _, files in os.walk(os.getcwd()):
        for file in files:
            if not file.endswith(inputFile):  # Input file
                continue
            file = os.path.join(root, file)
            allFiles.append(file)

    for file in allFiles:
        uv.addEggFile(file)
        uv.parseModel()

