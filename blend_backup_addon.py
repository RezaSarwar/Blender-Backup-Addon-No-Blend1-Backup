bl_info = {
    "name": "Save .blend Backup",
    "author": "RimuruDev",
    "version": (1, 2),
    "blender": (4, 4, 0),
    "location": "File > Save Backup",
    "description": "Creates *_backup.blend next to current file and disables .blend1",
    "category": "System",
}

import bpy, os, shutil
from bpy.app.handlers import persistent

@persistent
def save_post_handler(_):
    path = bpy.data.filepath
    if not path:
        return
    d, n = os.path.dirname(path), os.path.splitext(os.path.basename(path))[0]
    shutil.copy2(path, os.path.join(d, f"{n}_backup.blend"))

def manual_backup():
    path = bpy.data.filepath
    if not path:
        bpy.ops.wm.save_mainfile('INVOKE_DEFAULT')
        return
    d, n = os.path.dirname(path), os.path.splitext(os.path.basename(path))[0]
    shutil.copy2(path, os.path.join(d, f"{n}_backup.blend"))

class OT_SaveBackup(bpy.types.Operator):
    bl_idname = "wm.save_blend_backup"
    bl_label = "Save Backup (.blend)"
    bl_description = "Copy current .blend to *_backup.blend"

    def execute(self, _):
        manual_backup()
        return {'FINISHED'}

class OT_SaveAndBackup(bpy.types.Operator):
    bl_idname = "wm.save_and_backup"
    bl_label = "Save and Backup (.blend)"
    bl_description = "Save file and make *_backup.blend"

    def execute(self, _):
        if not bpy.data.filepath:
            bpy.ops.wm.save_mainfile('INVOKE_DEFAULT')
            return {'CANCELLED'}
        bpy.ops.wm.save_mainfile()
        manual_backup()
        return {'FINISHED'}

def draw_menu(self, _):
    self.layout.operator(OT_SaveBackup.bl_idname, icon='FILE_BACKUP')

addon_keymaps = []

def register():
    bpy.utils.register_class(OT_SaveBackup)
    bpy.utils.register_class(OT_SaveAndBackup)
    bpy.types.TOPBAR_MT_file.append(draw_menu)
    bpy.context.preferences.filepaths.save_version = 0
    if save_post_handler not in bpy.app.handlers.save_post:
        bpy.app.handlers.save_post.append(save_post_handler)

    kc = bpy.context.window_manager.keyconfigs.addon
    if kc:
        km = kc.keymaps.new(name='Window', space_type='EMPTY')
        addon_keymaps.extend([
            (km, km.keymap_items.new("wm.save_blend_backup", type='B', value='PRESS', ctrl=True, alt=True)),
            (km, km.keymap_items.new("wm.save_and_backup", type='S', value='PRESS', ctrl=True, shift=True)),
            (km, km.keymap_items.new("wm.save_and_backup", type='S', value='PRESS', oskey=True)),
        ])

def unregister():
    bpy.types.TOPBAR_MT_file.remove(draw_menu)
    bpy.utils.unregister_class(OT_SaveBackup)
    bpy.utils.unregister_class(OT_SaveAndBackup)
    if save_post_handler in bpy.app.handlers.save_post:
        bpy.app.handlers.save_post.remove(save_post_handler)
    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()

if __name__ == "__main__":
    register()
