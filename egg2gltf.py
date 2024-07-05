import bpy
import os, subprocess, sys, re


class BatchEgg2GLTF():
    def __init__(self):
        self.view_layer = bpy.context.view_layer
        self.mFilePath = None
        # scene = bpy.data.scenes.new("Scene")
        bpy.ops.object.select_all()
        bpy.ops.object.delete()  # Delete the default stuff
        pass

    def parseModel(self):
        # bpy.ops.object.select_all(action='SELECT')
        selection = bpy.context.selected_objects
        bpy.ops.object.select_all(action='DESELECT')
        if self.mFilePath is None:
            return
        for obj in selection:
            self.obj = obj
            obj.select_set(True)
            self.view_layer.objects.active = obj
            self.exportToGltf()
            #self.exportToFbx()
            bpy.ops.object.delete()
            
            
    def exportToGltf(self):
        lazyName = self.mFileName.replace(".egg", "")
        bpy.ops.export_scene.gltf(filepath=f"{self.mFilePath}/{lazyName}")
        
    def exportToFbx(self):
        # plugin specific
        lazyName = self.mFileName.replace(".egg", ".fbx")
        bpy.ops.export_scene.fbx(filepath=f"{self.mFilePath}/{lazyName}")


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
    converter = BatchEgg2GLTF()

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
        converter.addEggFile(file)
        converter.parseModel()


