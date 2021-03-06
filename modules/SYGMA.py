import matplotlib
import sys, os
sys.path.append('/usr/local/bin/NuPyCEE')
#temp fix
if os.path.isdir("/usr/local/bin/NuPyCEE"):
    os.environ["SYGMADIR"] = "/usr/local/bin/NuPyCEE"

import sygma as s

import widget_framework as framework
from widget_utils import float_text, auto_styles

#from IPython.html import widgets
import ipywidgets as widgets


from IPython.display import display, clear_output
from matplotlib import pyplot
import numpy
import shutil
from imp import load_source

def start_SYGMA():
    frame = framework.framework()
    #frame.set_default_display_style(padding="0.25em",background_color="white", border_color="LightGrey", border_radius="0.5em")
    #frame.set_default_io_style(padding="0.25em", margin="0.25em", border_color="LightGrey", border_radius="0.5em")
    frame.set_default_display_style(border="0.5em LightGrey")
    frame.set_default_io_style(margin="0.25em", border="0.5em LightGrey")
  

    tablist = ["sim_page", "plot_page", "custom_imf_page", "get_table_page"]
    yield_list = {"Analytic prescription":{"Delay":"yield_tables/agb_and_massive_stars_nugrid_MESAonly_fryer12delay.txt",
                  "Rapid":"yield_tables/agb_and_massive_stars_nugrid_MESAonly_fryer12rapid.txt",
                  #"Exclude neutron-alpha rich freeze-out":"yield_tables/isotope_yield_table_MESA_only_fryer12_exclnalpha.txt"}, 
		  "Mix":"yield_tables/agb_and_massive_stars_nugrid_MESAonly_fryer12mix.txt"},
                  "Ye=0.4982":{"Fallback at Ye":"yield_tables/agb_and_massive_stars_nugrid_MESAonly_ye.txt"}
                  #"Fallback motivated by GCE":"yield_tables/isotope_yield_table_MESA_only_ye_fallback.txt"}
		  }
    #group_style = {"border_style":"none", "border_radius":"0em"}
    group_style = {"border":"0em none","margin":" 0em 0em 0em 0em"}

    # width: width of input fields e.g. for Total stellar time
    text_box_style = {"width":"14em",'description_width':'initial'}
    #button_style = {"font_size":"1.25em", "font_weight":"bold"}
    button_style = {"font_weight":"bold",'description_width':'initial'} #no fontsize

    #first_tab_style = {"border_radius":"0em 0.5em 0.5em 0.5em"}
    first_tab_style = {"border":"0.5em"}
    #custom_imf_dir = os.environ["SYGMADIR"] + "/SYGMA_widget_imfs/"
    custom_imf_dir = "./SYGMA_widget_imfs/"

    default_custom_imf_text = "\n#File to define a custom IMF\n#Define your IMF in custom_imf\n#so that the return value represents\n#the chosen IMF value for the input mass\n\ndef custom_imf(mass):\n    #Salpeter IMF\n    return mass**-2.35\n"
    
    states_plot = ["plot_totmasses", "plot_mass", "plot_spectro", "plot_mass_range"]
    states_sim_plot = ["run_sim"] + states_plot
    states_cimf = ["custom_imf", "load_custom_imf"]
    states = states_sim_plot + states_cimf
    frame.add_state(states)
    
    #isotopes_all=['H-1','H-2','He-3','He-4','Li-7','B-11','C-12','C-13','N-14','N-15','O-16','O-17','O-18','F-19','Ne-20','Ne-21','Ne-22','Na-23','Mg-24','Mg-25','Mg-26','Al-27','Si-28','Si-29','Si-30','P-31','S-32','S-33','S-34','S-36','Cl-35','Cl-37','Ar-36','Ar-38','Ar-40','K-39','K-40','K-41','Ca-40','Ca-42','Ca-43','Ca-44','Ca-46','Ca-48','Sc-45','Ti-46','Ti-47','Ti-48','Ti-49','Ti-50','V-50','V-51','Cr-50','Cr-52','Cr-53','Cr-54','Mn-55','Fe-54','Fe-56','Fe-57','Fe-58','Co-59','Ni-58','Ni-60','Ni-61','Ni-62','Ni-64']
    isotopes_all=['H-1', 'H-2', 'He-3', 'He-4', 'Li-7', 'B-11', 'C-12', 'C-13', 'N-14', 'N-15', 'O-16', 'O-17', 'O-18', 'F-19', 'Ne-20', 'Ne-21', 'Ne-22', 'Na-23', 'Mg-24', 'Mg-25', 'Mg-26', 'Al-27', 'Si-28', 'Si-29', 'Si-30', 'P-31', 'Pb-206', 'Pb-207', 'S-32', 'S-33', 'S-34', 'S-36', 'Cl-35', 'Cl-37', 'Ar-36', 'Ar-38', 'Ar-40', 'K-39', 'K-40', 'K-41', 'Ca-40', 'Ca-42', 'Ca-43', 'Ca-44', 'Ca-46', 'Ca-48', 'Sc-45', 'Ti-46', 'Ti-47', 'Ti-48', 'Ti-49', 'Ti-50', 'V-50', 'V-51', 'Cr-50', 'Cr-52', 'Cr-53', 'Cr-54', 'Mn-55', 'Fe-54', 'Fe-56', 'Fe-57', 'Fe-58', 'Co-59', 'Ni-58', 'Ni-60', 'Ni-61', 'Ni-62', 'Ni-64', 'Cu-63', 'Cu-65', 'Zn-64', 'Zn-66', 'Zn-67', 'Zn-68', 'Zn-70', 'Ga-69', 'Ga-71', 'Ge-70', 'Ge-72', 'Ge-73', 'Ge-74', 'Ge-76', 'As-75', 'Se-74', 'Se-76', 'Se-77', 'Se-78', 'Se-80', 'Se-82', 'Br-79', 'Br-81', 'Kr-78', 'Kr-80', 'Kr-82', 'Kr-83', 'Kr-84', 'Kr-86', 'Rb-85', 'Rb-87', 'Sr-84', 'Sr-86', 'Sr-87', 'Sr-88', 'Y-89', 'Zr-90', 'Zr-91', 'Zr-92', 'Zr-94', 'Zr-96', 'Nb-93', 'Mo-92', 'Mo-94', 'Mo-95', 'Mo-96', 'Mo-97', 'Mo-98', 'Mo-100', 'Ru-96', 'Ru-98', 'Ru-99', 'Ru-100', 'Ru-101', 'Ru-102', 'Ru-104', 'Rh-103', 'Pd-102', 'Pd-104', 'Pd-105', 'Pd-106', 'Pd-108', 'Pd-110', 'Ag-107', 'Ag-109', 'Cd-106', 'Cd-108', 'Cd-110', 'Cd-111', 'Cd-112', 'Cd-113', 'Cd-114', 'Cd-116', 'In-113', 'In-115', 'Sn-112', 'Sn-114', 'Sn-115', 'Sn-116', 'Sn-117', 'Sn-118', 'Sn-119', 'Sn-120', 'Sn-122', 'Sn-124', 'Sb-121', 'Sb-123', 'Te-120', 'Te-122', 'Te-123', 'Te-124', 'Te-125', 'Te-126', 'Te-128', 'Te-130', 'I-127', 'Xe-124', 'Xe-126', 'Xe-128', 'Xe-129', 'Xe-130', 'Xe-131', 'Xe-132', 'Xe-134', 'Xe-136', 'Cs-133', 'Ba-130', 'Ba-132', 'Ba-134', 'Ba-135', 'Ba-136', 'Ba-137', 'Ba-138', 'La-138', 'La-139', 'Ce-136', 'Ce-138', 'Ce-140', 'Ce-142', 'Pr-141', 'Nd-142', 'Nd-143', 'Nd-144', 'Nd-145', 'Nd-146', 'Nd-148', 'Nd-150', 'Sm-144', 'Sm-147', 'Sm-148', 'Sm-149', 'Sm-150', 'Sm-152', 'Sm-154', 'Eu-151', 'Eu-153', 'Gd-152', 'Gd-154', 'Gd-155', 'Gd-156', 'Gd-157', 'Gd-158', 'Gd-160', 'Tb-159', 'Dy-156', 'Dy-158', 'Dy-160', 'Dy-161', 'Dy-162', 'Dy-163', 'Dy-164', 'Ho-165', 'Er-162', 'Er-164', 'Er-166', 'Er-167', 'Er-168', 'Er-170', 'Tm-169', 'Yb-168', 'Yb-170', 'Yb-171', 'Yb-172', 'Yb-173', 'Yb-174', 'Yb-176', 'Lu-175', 'Lu-176', 'Hf-174', 'Hf-176', 'Hf-177', 'Hf-178', 'Hf-179', 'Hf-180', 'Ta-180', 'Ta-181', 'W-180', 'W-182', 'W-183', 'W-184', 'W-186', 'Re-185', 'Re-187', 'Os-184', 'Os-186', 'Os-187', 'Os-188', 'Os-189', 'Os-190', 'Os-192', 'Ir-191', 'Ir-193', 'Pt-190', 'Pt-192', 'Pt-194', 'Pt-195', 'Pt-196', 'Pt-198', 'Au-197', 'Hg-196', 'Hg-198', 'Hg-199', 'Hg-200', 'Hg-201', 'Hg-202', 'Hg-204', 'Tl-203', 'Tl-205', 'Pb-204', 'Pb-208', 'Bi-209']
    #elements_all=['H','He','Li','B','C','N','O','F','Ne','Na','Mg','Al','Si','P','S','Cl','Ar','K','Ca','Sc','Ti','V','Cr','Mn','Fe','Co','Ni']
    elements_all=['H', 'He', 'Li', 'B', 'C', 'N', 'O', 'F', 'Ne', 'Na', 'Mg', 'Al', 'Si', 'P', 'Pb', 'S', 'Cl', 'Ar', 'K', 'Ca', 'Sc', 'Ti', 'V', 'Cr', 'Mn', 'Fe', 'Co', 'Ni', 'Cu', 'Zn', 'Ga', 'Ge', 'As', 'Se', 'Br', 'Kr', 'Rb', 'Sr', 'Y', 'Zr', 'Nb', 'Mo', 'Ru', 'Rh', 'Pd', 'Ag', 'Cd', 'In', 'Sn', 'Sb', 'Te', 'I', 'Xe', 'Cs', 'Ba', 'La', 'Ce', 'Pr', 'Nd', 'Sm', 'Eu', 'Gd', 'Tb', 'Dy', 'Ho', 'Er', 'Tm', 'Yb', 'Lu', 'Hf', 'Ta', 'W', 'Re', 'Os', 'Ir', 'Pt', 'Au', 'Hg', 'Tl', 'Bi']
    #isotopes_sn1a=['C-12','C-13','N-14','N-15','O-16','O-17','O-18','F-19','Ne-20','Ne-21','Ne-22','Na-23','Mg-24','Mg-25','Mg-26','Al-27','Si-28','Si-29','Si-30','P-31','S-32','S-33','S-34','S-36','Cl-35','Cl-37','Ar-36','Ar-38','Ar-40','K-39','K-40','K-41','Ca-40','Ca-42','Ca-43','Ca-44','Ca-46','Ca-48','Sc-45','Ti-46','Ti-47','Ti-48','Ti-49','Ti-50','V-50','V-51','Cr-50','Cr-52','Cr-53','Cr-54','Mn-55','Fe-54','Fe-56','Fe-57','Fe-58','Co-59','Ni-58','Ni-60','Ni-61','Ni-62','Ni-64']
    isotopes_sn1a=['C-12', 'C-13', 'N-14', 'N-15', 'O-16', 'O-17', 'O-18', 'F-19', 'Ne-20', 'Ne-21', 'Ne-22', 'Na-23', 'Mg-24', 'Mg-25', 'Mg-26', 'Al-27', 'Si-28', 'Si-29', 'Si-30', 'P-31', 'S-32', 'S-33', 'S-34', 'S-36', 'Cl-35', 'Cl-37', 'Ar-36', 'Ar-38', 'Ar-40', 'K-39', 'K-41', 'Ca-40', 'Ca-42', 'Ca-43', 'Ca-44', 'Ca-46', 'Ca-48', 'Sc-45', 'Ti-46', 'Ti-47', 'Ti-48', 'Ti-49', 'Ti-50', 'V-50', 'V-51', 'Cr-50', 'Cr-52', 'Cr-53', 'Cr-54', 'Mn-55', 'Fe-54', 'Fe-56', 'Fe-57', 'Fe-58', 'Co-59', 'Ni-58', 'Ni-60', 'Ni-61', 'Ni-62', 'Ni-64', 'Cu-63', 'Cu-65', 'Zn-64', 'Zn-66', 'Zn-67', 'Zn-68', 'Zn-70', 'Ga-69', 'Ga-71', 'Ge-70', 'Ge-72', 'Ge-73', 'Ge-74']
    #elements_sn1a=['C','N','O','F','Ne','Na','Mg','Al','Si','P','S','Cl','Ar','K','Ca','Sc','Ti','V','Cr','Mn','Fe','Co','Ni']
    elements_sn1a=['C', 'N', 'O', 'F', 'Ne', 'Na', 'Mg', 'Al', 'Si', 'P', 'S', 'Cl', 'Ar', 'K', 'Ca', 'Sc', 'Ti', 'V', 'Cr', 'Mn', 'Fe', 'Co', 'Ni', 'Cu', 'Zn', 'Ga', 'Ge']
    isotopes_sel_mult = ["All"] + isotopes_all
    elements_sel_mult = ["All"] + elements_all
    
    line_styles=["-", "--", ":", "-."]
#    line_colors=["k", "r", "g", "b", "c", "m", "y"]
    line_colors=["k", "r", "b", "c", "m", "y"]#remove "g"
    line_markers = ["o", "s", "x", "D", "v", "^", "<", ">", "p", "*", "+"]
    
    styles = auto_styles()
    styles.set_line_styles(line_styles)
    styles.set_line_colors(line_colors)
    styles.set_line_markers(line_markers)

    frame.set_state_data("elements", elements_all)
    frame.set_state_data("isotopes", isotopes_all)
    frame.set_state_data("over_plotting_data", [])    
    frame.set_state_data("styles", styles)
    frame.set_state_data("old_state", None)
    
    frame.set_state_data("runs", [])
    frame.set_state_data("run_count", 0)
    
    def add_run(data, name, Z):
	'''
	Save SYGMA instance and other information of successfull run. Add to stack of previous simulations.
	'''

        run_count = frame.get_state_data("run_count")
        runs_data = frame.get_state_data("runs")
        widget_name = "runs_widget_#"+str(run_count)
        
        frame.add_io_object(widget_name)
        frame.set_state_attribute(widget_name, visibility='visible', description=name)
        frame.set_object(widget_name, widgets.ToggleButton(button_style = 'info'))
        
        runs_data.append((data, name, Z, widget_name))
        frame.set_state_children("runs", [widget_name])
        frame.set_state_data("runs", runs_data)
        run_count += 1
        frame.set_state_data("run_count", run_count)
    
    def remove_runs():
        data = frame.get_state_data("runs")
        children = ["runs_title"]
        tmp_data = []
        for i in xrange(len(data)):
            widget_name = data[i][3]
            if frame.get_attribute(widget_name, "value"):
                frame.remove_object(widget_name)
            else:
                children.append(widget_name)
                tmp_data.append(data[i])
        data = tmp_data
        frame.set_state_children("runs", children, append=False)
        frame.set_state_data("runs", data)
        
    def list_custom_imf():
        if os.path.isdir(custom_imf_dir):
            files_dirs = os.listdir(custom_imf_dir)
            imfs = []
            for file in files_dirs:
                file_full = custom_imf_dir + file
                if os.path.isfile(file_full):
                    file = file.rsplit(".", 1)
                    if file[1] == "py":
                        imfs.append(file[0])
            return imfs
        else:
            return []
    
    frame.add_display_object("window")
    #frame.add_io_object("title")
    frame.add_display_object("widget_runs_group")
    frame.add_display_object("widget")

    frame.add_display_object("runs")
    frame.add_io_object("runs_title")
    
    ###Sim page###
    frame.add_display_object("sim_page")
    
    frame.add_display_object("mass_Z_group")
    frame.add_io_object("init_Z")
    frame.add_io_object("mass_gas")
    
    frame.add_display_object("time_group")
    frame.add_io_object("t_end")
    frame.add_io_object("dt")
    
    frame.add_display_object("imf_type_group")
    frame.add_io_object("imf_type")
    frame.add_io_object("imf_alpha")
    
    frame.add_display_object("imf_mass_group")
    frame.add_io_object("imf_mass_min")
    frame.add_io_object("imf_mass_max")
    
    frame.add_display_object("sn1a_group")
    frame.add_io_object("use_sn1a")
    frame.add_io_object("sn1a_rates")
    
    frame.add_display_object("yield_table_group")
    frame.add_io_object("yield_table_selection")
    frame.add_io_object('yeild_table_label')
    frame.add_io_object("yield_table_list")

    frame.add_display_object("run_sim_remove_run_group")
    frame.add_io_object("run_sim")
    frame.add_io_object("remove_run")
    frame.add_io_object("run_name")
    
    frame.add_io_object("plot_type")
    frame.add_io_object("sim_responce")

    # define relation between display widgets and children
    #frame.set_state_children("window", ["title", "widget_runs_group"])
    frame.set_state_children("window", ["widget_runs_group"])

    frame.set_state_children("widget_runs_group", ["widget", "runs"])

    frame.set_state_children("widget", ["sim_page"], titles=["Simulation"])
    frame.set_state_children("sim_page", ["mass_Z_group", "time_group", "imf_type_group", "imf_mass_group", "sn1a_group", "yield_table_group", "run_sim_remove_run_group", "sim_responce"])
    frame.set_state_children("mass_Z_group", ["mass_gas", "init_Z"])
    frame.set_state_children("time_group", ["t_end", "dt"])
    frame.set_state_children("imf_type_group", ["imf_type", "imf_alpha"])
    frame.set_state_children("imf_mass_group", ["imf_mass_min", "imf_mass_max"])
    frame.set_state_children("sn1a_group", ["use_sn1a", "sn1a_rates"])
    frame.set_state_children("yield_table_group", ["yeild_table_label","yield_table_selection","yield_table_list"])
    frame.set_state_children("run_sim_remove_run_group", ["run_sim", "remove_run", "run_name"])
    
    frame.set_state_children("runs", ["runs_title"])
    
    ###plotting page###
    frame.add_display_object("plot_page")
    
    #frame.add_io_object("warning_msg")
    frame.add_io_object("plot_name")
    
    frame.add_display_object("source_over_plotting_group")
    frame.add_io_object("source")
    frame.add_io_object("over_plotting")
    frame.add_io_object("clear_plot")
    
    frame.add_display_object("species_group")
    frame.add_display_object("plot_commands")
    frame.add_io_object("iso_or_elem")
    frame.add_io_object("iso_or_elem2")
    frame.add_io_object("species")
    
    #frame.add_io_object("elem_numer")
    frame.add_io_object("elem_denom")
    frame.add_io_object("plot")

    # define relation between display widgets and children
    frame.set_state_children("widget", ["plot_page"], titles=["Plotting"])
    frame.set_state_children("plot_page", ["plot_type", "plot_name", "source_over_plotting_group", "species_group", "elem_denom","plot_commands"])
    frame.set_state_children("source_over_plotting_group", ["source"])
    frame.set_state_children("species_group", ["iso_or_elem", "species"])
    frame.set_state_children("plot_commands", ["over_plotting", "clear_plot","plot"])    
    
    ###Custom IMF page###
    frame.add_display_object("custom_imf_page")
    
    frame.add_display_object("load_save_imf_group")
    frame.add_io_object("load_imf")
    frame.add_io_object("list_imfs")
    frame.add_io_object("name_imf")
    frame.add_io_object("save_imf")
    frame.add_io_object("delete_imf")
    
    frame.add_io_object("text_imf")
    
    frame.add_io_object("test_imf")

    # define relation between display widgets and children
    frame.set_state_children("widget", ["custom_imf_page"], titles=["Custom IMF"])
    frame.set_state_children("custom_imf_page", ["load_save_imf_group", "text_imf", "test_imf"])
    frame.set_state_children("load_save_imf_group", ["load_imf", "list_imfs", "name_imf", "save_imf", "delete_imf"])


    ###plotting page###
    frame.add_display_object("get_table_page")

    frame.add_display_object("species_mult_group")
    frame.add_io_object("species_mult")
    
    frame.add_io_object("get_table")
    frame.add_io_object("table_links")
    
    # define relation between display widgets and children
    frame.set_state_children("widget", ["get_table_page"], titles=["Download Tables"])
    frame.set_state_children("get_table_page", ["species_mult_group", "get_table", "table_links"])
    frame.set_state_children("species_mult_group", ["iso_or_elem2", "species_mult"])
        
            
    #set layout of interface
    frame.set_state_attribute('window',visibility='visible', **group_style)
    #frame.set_state_attribute('title', visibility='visible', value="<center><h1>SYGMA<br></h1></center>",margin="3.15em 3.5em 3.5em 3.5em")
    frame.set_state_attribute("runs_title", visibility='visible', value="<p><h4>Runs</h4></p>", margin="0em 0em 0em 4em",border="5em none")
    frame.set_state_attribute("runs", visibility='visible',margin="0em 0em 0em 0em",border="0em none")
    
    
    frame.set_state_attribute("widget_runs_group", visibility='visible', **group_style)
    frame.set_state_attribute('widget', visibility='visible', **group_style)
    frame.set_state_attribute("runs", states_cimf, visibility='hidden')
      
    frame.set_state_attribute('sim_page', visibility='visible', **first_tab_style)
    frame.set_state_attribute("mass_Z_group", visibility='visible', **group_style)
    frame.set_state_attribute("mass_gas", visibility='visible', description="Total stellar mass [$M_{\odot}$]:", value="1.0", **text_box_style)
    frame.set_state_attribute('init_Z', visibility='visible', description="Initial metallicity: ", options=["0.02", "0.01", "0.006", "0.001", "0.0001", "0.0"], **text_box_style)
    
    frame.set_state_attribute('time_group', visibility='visible', **group_style)
    frame.set_state_attribute('t_end', visibility='visible', description="Final time [yr]: ", value="1.0e10", **text_box_style)
    frame.set_state_attribute('dt', visibility='visible', description="Time step [yr]: ", value="1.0e7", **text_box_style)
    
    frame.set_state_attribute('imf_type_group', visibility='visible', **group_style)
    frame.set_state_attribute('imf_type', visibility='visible', description="IMF type: ", options=['salpeter', 'chabrier', 'kroupa', 'alphaimf'] + list_custom_imf(),**text_box_style)
    frame.set_state_attribute('imf_alpha', description="Set alpha: ", min=0, max=5)
    
    frame.set_state_attribute("imf_mass_group", visibility='visible', **group_style)
    frame.set_state_attribute('imf_mass_min', visibility='visible', description="IMF lower limit [$M_{\odot}$]: ", value="1.0", **text_box_style)
    frame.set_state_attribute('imf_mass_max', visibility='visible', description="IMF upper limit [$M_{\odot}$]: ", value="30.0", **text_box_style)
    
    frame.set_state_attribute('sn1a_group', visibility='visible', **group_style)
    frame.set_state_attribute('use_sn1a', visibility='visible', description="Include SNe Ia: ", value=True)
    frame.set_state_attribute("yield_table_group", visibility='visible', **group_style)
    frame.set_state_attribute("yeild_table_label", visibility ='visible',description="CCSN remnant prescription:")
    frame.set_state_attribute("yield_table_selection", visibility='visible', options=["Analytic prescription", "Ye=0.4982"], value="Analytic prescription", **text_box_style)
    #frame.set_state_attribute('yield_table_list', visibility='visible', description="CCSN remnant prescription:",width = '400px', options=yield_list["Analytic prescription"], selected_label="Delay")
    frame.set_state_attribute('yield_table_list', visibility='visible', options=yield_list["Analytic prescription"], selected_label="Delay")
    frame.set_state_links("sn1a_link", [("use_sn1a", "visibility"), ("sn1a_rates", "visibility")], directional=True) #changed value to visibiltiy
    
    frame.set_state_attribute('sn1a_rates', description="SNe Ia rates: ", options=['Power law', 'Exponential', 'Gaussian','Maoz12'],**text_box_style)
    
    frame.set_state_attribute("run_sim_remove_run_group", visibility='visible', **group_style)
    frame.set_state_attribute('run_sim', visibility='visible', description="Run simulation", **button_style)
    frame.set_state_attribute("remove_run", visibility='visible', description="Remove selected", **button_style)
    frame.set_state_attribute("run_name", visibility='visible', description="Run name: ", placeholder="Enter name", value="", **text_box_style)
    
    frame.set_state_attribute("sim_responce", value="<p>Simulation data loaded.</p>", **group_style)
    frame.set_state_attribute("sim_responce", states_sim_plot, visibility='visible')
    
    frame.set_state_attribute('plot_type', states_sim_plot, visibility='visible', description="Plot type: ", options=["Total mass", "Species mass", "Species spectroscopic", "Mass range contributions"])
    
    def mass_gas_handler(name, value):
        frame.set_attributes("mass_gas", value=float_text(value))
    
    def t_end_handler(name, value):
        frame.set_attributes("t_end", value=float_text(value))
    
    def dt_handler(name, value):
        frame.set_attributes("dt", value=float_text(value))
    
    def imf_mass_min_handler(name, value):
        frame.set_attributes("imf_mass_min", value=float_text(value))
    
    def imf_mass_max_handler(name, value):
        frame.set_attributes("imf_mass_max", value=float_text(value))
    
    def sel_imf_type(attribute, value):
        if value=="alphaimf":
            frame.set_state_attribute("imf_alpha", visibility='visible')
            frame.set_attributes("imf_alpha", visibility='visible', value=2.35)
        else:
            frame.set_state_attribute("imf_alpha", visibility='hidden')
            frame.set_attributes("imf_alpha", visibility='hidden')
            
    def yield_table_selection_handler(name, value):
        frame.set_attributes("yield_table_list", options=yield_list[value])
        
        if value == "Analytic prescription":

            frame.set_attributes("yield_table_list", selected_label="Delay",**text_box_style)
        elif value == "Ye=0.4982":
            frame.set_attributes("yield_table_list", selected_label="Fallback at Ye")        
    
    def run_simulation(widget):
	'''
	   Run the simulation. Retrieve atributes as input for SYGMA and run SYGMA.
	'''

        frame.set_attributes("sim_responce", visibility='hidden')
        #clear_output(wait=True) #closing the window widget
        pyplot.close("all")
        
        sn1a_map = {"Power law":"power_law", "Gaussian":"gauss","Exponential":"exp","Maoz12":"maoz"}
        
        mgal = float(frame.get_attribute("mass_gas", "value"))
        iniZ = float(frame.get_attribute("init_Z", "value"))
        imf_type = frame.get_attribute("imf_type", "value")
        alphaimf = frame.get_attribute("imf_alpha", "value")
        mass_min = float(frame.get_attribute("imf_mass_min", "value"))
        mass_max = float(frame.get_attribute("imf_mass_max", "value"))
        imf_bdys = [mass_min, mass_max]
        sn1a_on = frame.get_attribute("use_sn1a", "value")
        sn1a_rate = sn1a_map[frame.get_attribute("sn1a_rates", "value")]
        dt = float(frame.get_attribute("dt", "value"))
        tend = float(frame.get_attribute("t_end", "value"))
        yield_table = frame.get_attribute("yield_table_list", "value")
        
        if not (imf_type in ['salpeter', 'chabrier', 'kroupa', 'alphaimf']):
            #destination = os.environ["SYGMADIR"] + "/imf_input.py"
	    destination = "./imf_input.py"
            shutil.copy(custom_imf_dir + imf_type + ".py", destination)
            imf_type = "input"
        
        run_count = frame.get_state_data("run_count")
        name = frame.get_attribute("run_name", "value")
        if name == "":
            name = "Run - "+"%03d" % (run_count + 1, )
       	import sys 
	#sys.stdout = open(os.devnull, 'w')
	if iniZ==0.0:
		data=s.sygma(mgal=mgal, iniZ=iniZ, imf_type=imf_type, alphaimf=alphaimf, imf_bdys=[10.1, 100.0], imf_bdys_pop3=imf_bdys, sn1a_on=sn1a_on,
			  sn1a_rate=sn1a_rate, dt=dt,tend=tend, table=yield_table)
	else:
		data=s.sygma(mgal=mgal, iniZ=iniZ, imf_type=imf_type, alphaimf=alphaimf, imf_bdys=imf_bdys, sn1a_on=sn1a_on,
		 sn1a_rate=sn1a_rate, dt=dt,tend=tend, table=yield_table)
	#sys.stdout = sys.__stdout__
        frame.set_state("run_sim")
        ##force reset plottype
        frame.set_attributes("plot_type", selected_label="Species mass", value="Species mass")
        frame.set_attributes("plot_type", selected_label="Total mass", value="Total mass")
       
        #save simulation, results and name.
        add_run(data, name, iniZ)

	#add attributes, widgets back to default.
        frame.update()
	#frame.display_object("window",state=frame._state)
	#display(frame._object_list["window"])
	#display(self._object_list["window"])


    def remove_simulation(widget):
        remove_runs()
        frame.update()    
        
    def sel_tab(name, value):
       '''
       Set state, data etc. corresponding to tab selected.
       '''

       open_tab = tablist[value]
       
       if open_tab == "custom_imf_page":
           frame.set_state_data("old_state", frame.get_state())
           frame.set_state("custom_imf")
           if frame.get_attribute("name_imf", "value") == "":
		   frame.set_attributes("text_imf", value=default_custom_imf_text,width='20em',height='20em',right='0em',margin="0em 0em 0em 0em")
       else:
           if frame.get_state() in states_cimf:
               old_state = frame.get_state_data("old_state")
               if old_state != None:
                   frame.set_state(old_state)
               else:
                   frame.set_state("default")
               frame.set_state_data("old_state", None)
       #print 'sel_tab, set state:',frame._state
  
    # set callbacks/functions
    frame.set_state_callbacks("mass_gas", mass_gas_handler)        
    frame.set_state_callbacks("t_end", t_end_handler)        
    frame.set_state_callbacks("dt", dt_handler)        
    frame.set_state_callbacks("imf_mass_min", imf_mass_min_handler)
    frame.set_state_callbacks("imf_mass_max", imf_mass_max_handler)
    frame.set_state_callbacks("imf_type", sel_imf_type)
    frame.set_state_callbacks("yield_table_selection", yield_table_selection_handler)
    frame.set_state_callbacks("run_sim", run_simulation, attribute=None, type="on_click")
    frame.set_state_callbacks("remove_run", remove_simulation, attribute=None, type="on_click")
    frame.set_state_callbacks("widget", sel_tab, "selected_index")
    
    frame.set_object("window", widgets.Box())
    #frame.set_object("title", widgets.HTML())
    frame.set_object("widget_runs_group", widgets.HBox())
    frame.set_object("widget", widgets.Tab())
    frame.set_object("runs", widgets.VBox())

    frame.set_object("runs_title", widgets.HTML())
    
    frame.set_object("sim_page", widgets.VBox())
    frame.set_object("mass_Z_group", widgets.HBox())
    frame.set_object("mass_gas", widgets.Text())
    frame.set_object("init_Z", widgets.Dropdown())
    
    frame.set_object("time_group", widgets.HBox())
    frame.set_object("t_end", widgets.Text())
    frame.set_object("dt", widgets.Text())
    
    frame.set_object("imf_type_group", widgets.HBox())
    frame.set_object("imf_type", widgets.Dropdown())
    frame.set_object("imf_alpha", widgets.FloatSlider())
    
    frame.set_object("imf_mass_group", widgets.HBox())
    frame.set_object("imf_mass_min", widgets.Text())
    frame.set_object("imf_mass_max", widgets.Text())
    
    frame.set_object("sn1a_group", widgets.HBox())
    frame.set_object("use_sn1a", widgets.Checkbox())
    frame.set_object("sn1a_rates", widgets.Dropdown())
    
    frame.set_object("yield_table_group", widgets.HBox())
    frame.set_object("yield_table_selection", widgets.ToggleButtons())
    frame.set_object("yeild_table_label",widgets.Label(value="CCSN remnant prescription:"))
    frame.set_object("yield_table_list", widgets.Dropdown(layout= widgets.Layout(width = '110px')))
    
    frame.set_object("run_sim_remove_run_group", widgets.HBox())
    frame.set_object("run_sim", widgets.Button())
    frame.set_object("remove_run", widgets.Button())
    frame.set_object("run_name", widgets.Text())
    
    frame.set_object("sim_responce", widgets.HTML())
    
    frame.set_object("plot_type", widgets.Dropdown())
    
    
    frame.set_state_attribute("plot_page", visibility='visible')
    #frame.set_state_attribute("warning_msg", visibility='visible', value="<h3>Error: No simulation data!</h3>", **group_style)
    #frame.set_state_attribute("warning_msg", states_plot, visibility='hidden')
    frame.set_state_attribute("plot_name", **group_style)
    frame.set_state_attribute("plot_name", visibility='visible', value="<h3>Error: No simulation data!</h3>")
    frame.set_state_attribute("plot_name", "plot_totmasses", visibility='visible', value="<h2>Plot: Total mass evolution</h2>")
    frame.set_state_attribute("plot_name", "plot_mass", visibility='visible', value="<h2>Plot: Species mass evolution</h2>")
    frame.set_state_attribute("plot_name", "plot_spectro", visibility='visible', value="<h2>Plot: Spectroscopic Mass evolution</h2>")
    frame.set_state_attribute("plot_name", "plot_mass_range", visibility='visible', value="<h2>Plot: Mass range contributions</h2><p>Only ejecta from AGB and massive stars are considered.</p>")
    
    frame.set_state_attribute("source_over_plotting_group", states_plot, visibility='visible', **group_style)
    frame.set_state_attribute("source", ["plot_totmasses", "plot_mass", "plot_spectro"], visibility='visible', description="Yield source: ", options=["All", "AGB", "SNe Ia", "Massive"], selected_label="All")
    frame.set_state_attribute("over_plotting", visibility='visible', description="Over plotting", value=False, **button_style)
    frame.set_state_attribute("clear_plot", description="Clear plot", **button_style)
    frame.set_state_links("clear_plot_link", [("over_plotting", "visibility"),("clear_plot", "visibility")], directional=True) #changd value to visibiliy
    
    frame.set_state_attribute("species_group", ["plot_mass", "plot_mass_range"], visibility='visible', **group_style)
    frame.set_state_attribute("plot_commands",visibility='visible', **group_style)
    frame.set_state_attribute("iso_or_elem",["plot_mass", "plot_mass_range","plot_spectro"], visibility='visible', description="species type: ", options=["Elements", "Isotopes"], selected_label="Elements")
    frame.set_state_attribute("iso_or_elem",["plot_totmasses","plot_spectro"], visibility='hidden', description="species type: ", options=["Elements", "Isotopes"], selected_label="Elements")
    frame.set_state_attribute("species",["plot_mass", "plot_mass_range"], visibility='visible', description="Element: ", options=elements_all, **text_box_style)
    frame.set_state_attribute("species", "plot_spectro", visibility='visible', description="Y-axis [X/Y], choose X: ", options=elements_all, **text_box_style)
    frame.set_state_attribute("elem_denom", "plot_spectro", visibility='visible', description="Y-axis [X/Y], choose Y: ", options=elements_all, **text_box_style)
    frame.set_state_attribute("plot", states_plot, visibility='visible', description="Generate plot", **button_style)
    #frame.set_state_attribute("plot", visibility='visible', description="Generate Plot", **button_style)
    #frame.set_state_attribute("plot", states_plot, visibility='visible', description="Generate Plot", **button_style)

    def clear_plot_handler(widget):
        clear_output(wait=True)
        pyplot.close('all')
        display(frame._object_list['window']) #CR
        #clear_output(wait=True)
        #pyplot.close("all")
        #frame.set_state_data("over_plotting_data", [])
    
    def sel_plot_type(attribute, value):
        if value=="Total mass":
            frame.set_state("plot_totmasses")
        elif value=="Species mass":
            frame.set_state("plot_mass")
        elif value=="Species spectroscopic":
            frame.set_state("plot_spectro")
        elif value=="Mass range contributions":
            frame.set_state("plot_mass_range")
	#print 'sel_plot_type, set state:',frame._state
       
#        iniZ = float(frame.get_attribute("init_Z", "value"))
#        if iniZ==0.0:
#            frame.set_attributes("source", options=["All", "AGB", "Massive"])
#        else:
        frame.set_attributes("source", options=["All", "AGB", "SNe Ia", "Massive"])
        frame.set_state_data("over_plotting_data", [])
    
    def sel_source(attribute, value):
        if value=="SNe Ia":
            frame.set_state_data("elements", elements_sn1a)
            frame.set_state_data("isotopes", isotopes_sn1a)
        else:
            frame.set_state_data("elements", elements_all)
            frame.set_state_data("isotopes", isotopes_all)
            #frame.set_attributes("elem_numer", options=[])
            frame.set_attributes("elem_denom", options=[])
            frame.set_attributes("species", options=[])
    
        elements = frame.get_state_data("elements")
        isotopes = frame.get_state_data("isotopes")
        #frame.set_attributes("elem_numer", options=elements)
        frame.set_attributes("elem_denom", options=elements)
        
        if frame.get_attribute("iso_or_elem", "value")=="Isotopes":
            frame.set_attributes("species", description="Isotope: ", options=isotopes)
        elif frame.get_attribute("iso_or_elem", "value")=="Elements":
            frame.set_attributes("species", description="Element: ", options=elements)
    
    def sel_iso_or_elem(attribute, value):
        elements = frame.get_state_data("elements")
        isotopes = frame.get_state_data("isotopes")
        if value=="Isotopes":
            frame.set_attributes("species", description="Isotope: ", options=isotopes)
            frame.set_attributes("species_mult", description="Isotope: ", options=isotopes_sel_mult)
        elif value=="Elements":
            frame.set_attributes("species", description="Element: ", options=elements)
            frame.set_attributes("species_mult", description="Element: ", options=elements_sel_mult)
        
    def run(widget):

        #styles = frame.get_state_data("styles")
        #styles.reset_line_count()
   
  
   	#one of these two close widget window
        clear_output(wait=True)
        pyplot.close("all")
	#display here
	display(frame._object_list["window"]) #CR
	#pyplot.figure()
	#pyplot.plot([1,2,3],[3,1,2])
	#return 

        over_plotting = frame.get_attribute("over_plotting", "value")
        source_map = {"All":"all", "AGB":"agb", "SNe Ia":"sn1a", "Massive":"massive"}
        label_map = {"All":"", "AGB":", AGB", "SNe Ia":", SNIa", "Massive":", Massive"}
        tot_mass_labels = {"all":"All", "agb":"AGB", "sn1a":"SNIa", "massive":"Massive"}
        state = frame.get_state()
        runs = frame.get_state_data("runs")
        source = source_map[frame.get_attribute("source", "value")]
        label_source = label_map[frame.get_attribute("source", "value")]
        species = frame.get_attribute("species", "value")
        no_runs = True
        
        if state=="plot_totmasses":
            plot_data = frame.get_state_data("over_plotting_data")
            
            if not over_plotting:
                plot_data = []
            
            over_plot = [("source", source)]
            if not over_plot in plot_data:
                plot_data.append(over_plot)
                frame.set_state_data("over_plotting_data", plot_data)
            for data, name, Z, widget_name in runs:
                if frame.get_attribute(widget_name, "value"):
                    no_runs = False
                    for item in plot_data:
                        kwargs = dict(item)
                        label = name + ": " + tot_mass_labels[kwargs["source"]]
                        kwargs.update({"label":label})
                        kwargs.update(styles.get_style())
                        data.plot_totmasses(**kwargs)
			try:
				ax_tmp2=matplotlib.pyplot.gca()
				x1,x2,y1,y2=ax_tmp2.axis()			
				if x1>x11: x1 = x11
				if x2<x22: x2 = x22
				if y1>y11: y1 = y11
				if y2<y22: y2 = y22
				ax_tmp2.set_xlim(x1,x2)
				ax_tmp2.set_ylim(y1,y2)	
			except:
				pass
			x11,x22,y11,y22=matplotlib.pyplot.gca().axis()
	    #return
	elif state=="plot_mass":
            plot_data = frame.get_state_data("over_plotting_data")
            
            if not over_plotting:
                plot_data = []
            
            over_plot = [("specie", species), ("source", source)]
            if not over_plot in plot_data:
                plot_data.append(over_plot)
                frame.set_state_data("over_plotting_data", plot_data)
            
            for data, name, Z, widget_name in runs:
                if frame.get_attribute(widget_name, "value"):
                    no_runs = False
                    for item in plot_data:
                        kwargs = dict(item)
                        label = name + ": " + kwargs["specie"]
                        if not kwargs["source"] == "all":
                            label = label + ", " + tot_mass_labels[kwargs["source"]]
                        kwargs.update({"label":label})
                        kwargs.update(styles.get_style())
                        data.plot_mass(**kwargs)
			try:
				ax_tmp2=matplotlib.pyplot.gca()
				x1,x2,y1,y2=ax_tmp2.axis()			
				if x1>x11: x1 = x11
				if x2<x22: x2 = x22
				if y1>y11: y1 = y11
				if y2<y22: y2 = y22
				ax_tmp2.set_xlim(x1,x2)
				ax_tmp2.set_ylim(y1,y2)	
			except:
				pass
			x11,x22,y11,y22=matplotlib.pyplot.gca().axis()
        elif state=="plot_spectro":
            
            X = frame.get_attribute("species", "value")
            Y = frame.get_attribute("elem_denom", "value")
            yaxis = "["+X+"/"+Y+"]"

            plot_data = frame.get_state_data("over_plotting_data")
            
            if not over_plotting:
                plot_data = []
            
            over_plot = [("yaxis", yaxis), ("source", source)]
            if not over_plot in plot_data:
                plot_data.append(over_plot)
                frame.set_state_data("over_plotting_data", plot_data)
            
            for data, name, Z, widget_name in runs:
                if frame.get_attribute(widget_name, "value"):
                    no_runs = False
                    for item in plot_data:
                        kwargs = dict(item)
                        label = name + ": " + kwargs["yaxis"] + ", " + tot_mass_labels[kwargs["source"]]
                        kwargs.update({"label":label})
                        kwargs.update(styles.get_style())
                        data.plot_spectro(**kwargs)
			try:
				ax_tmp2=matplotlib.pyplot.gca()
				x1,x2,y1,y2=ax_tmp2.axis()			
				if x1>x11: x1 = x11
				if x2<x22: x2 = x22
				if y1>y11: y1 = y11
				if y2<y22: y2 = y22
				ax_tmp2.set_xlim(x1,x2)
				ax_tmp2.set_ylim(y1,y2)	
			except:
				pass
			x11,x22,y11,y22=matplotlib.pyplot.gca().axis()
	    #display(frame._object_list["window"]) #CR

        elif state=="plot_mass_range":
            plot_data = frame.get_state_data("over_plotting_data")
            
            if not over_plotting:
                plot_data = []
            
            over_plot = [("specie", species)]
            if not over_plot in plot_data:
                plot_data.append(over_plot)
                frame.set_state_data("over_plotting_data", plot_data)
            
            for data, name, Z, widget_name in runs:
                if frame.get_attribute(widget_name, "value"):
                    no_runs = False
                    for item in plot_data:
                        kwargs = dict(item)
                        label = name + ": " + kwargs["specie"]
                        kwargs.update({"label":label})
                        kwargs.update(styles.get_style())
                        data.plot_mass_range_contributions(**kwargs)
			try:
				ax_tmp2=matplotlib.pyplot.gca()
				x1,x2,y1,y2=ax_tmp2.axis()			
				if x1>x11: x1 = x11
				if x2<x22: x2 = x22
				if y1>y11: y1 = y11
				if y2<y22: y2 = y22
				ax_tmp2.set_xlim(x1,x2)
				ax_tmp2.set_ylim(y1,y2)	
			except:
				pass
			x11,x22,y11,y22=matplotlib.pyplot.gca().axis()
        if no_runs:
            print "No runs selected."                

    
    frame.set_state_callbacks("clear_plot", clear_plot_handler, attribute=None, type="on_click")
    frame.set_state_callbacks("plot_type", sel_plot_type)
    frame.set_state_callbacks("source", sel_source, state=["plot_spectro", "plot_mass"])
    frame.set_state_callbacks("iso_or_elem", sel_iso_or_elem)
    frame.set_state_callbacks("iso_or_elem2", sel_iso_or_elem)
    frame.set_state_callbacks("plot", run, attribute=None, type="on_click") #closes?


    frame.set_object("plot_page", widgets.VBox())
    #frame.set_object("warning_msg", widgets.HTML())
    frame.set_object("plot_name", widgets.HTML())
    frame.set_object("source_over_plotting_group", widgets.HBox())
    frame.set_object("source", widgets.Dropdown())
    frame.set_object("over_plotting", widgets.ToggleButton())
    frame.set_object("clear_plot", widgets.Button())
    frame.set_object("species_group", widgets.VBox())
    frame.set_object("plot_commands", widgets.HBox())
    frame.set_object("iso_or_elem", widgets.RadioButtons())
    frame.set_object("iso_or_elem2", widgets.RadioButtons())
    frame.set_object("species", widgets.Select())
    #frame.set_object("elem_numer", widgets.Select())
    frame.set_object("elem_denom", widgets.Select())
    frame.set_object("plot", widgets.Button())


    frame.set_state_attribute("custom_imf_page", visibility='visible')
    frame.set_state_attribute("load_save_imf_group", visibility='visible',width='45em')#, **group_style)
    frame.set_state_attribute("load_imf", "custom_imf", visibility='visible', description="Load custom IMF",width='18em',**button_style) #description_width='initial',width='10em') #, **button_style)
    frame.set_state_attribute("list_imfs", "load_custom_imf", visibility='visible', description="Select IMF",description_width='initial')
    frame.set_state_attribute("name_imf", "custom_imf", visibility='visible', description="IMF name",right='4em',width="8em",description_width='initial')#,left = '0em') #, **text_box_style)
    frame.set_state_attribute("save_imf", "custom_imf", visibility='visible', description="Save IMF",right='3em',width='10em',description_width='initial') #,right = '15em',height='5em',top='10em')#, **button_style)
    frame.set_state_attribute("delete_imf", "custom_imf", visibility='visible', description="Delete IMF",right='2em', width='10em') #description_width='initial')
  #,right = '15em',height='5em',top='10em')#, **button_style)

    frame.set_state_attribute("text_imf", visibility='visible')

    frame.set_state_attribute("test_imf", visibility='visible', description="Test selected IMF", **button_style)

    def load_imf_handler(widget):
        frame.set_state("load_custom_imf")
	#print 'load_imf_handler, set state: ',frame._state
        options = ["", "Preset: default"] + list_custom_imf()
        frame.set_attributes("list_imfs", options=options, value="", selected_label="")
    
    def sel_custom_imf(name, value):
        if value != "":
            frame.set_state("custom_imf")
	    #print 'sel_custom_imf: set state: ',frame._state
            if value == "Preset: default":
                frame.set_attributes("name_imf", value="")
                frame.set_attributes("text_imf", value=default_custom_imf_text)
            else:
                text = ""
                with open(custom_imf_dir + value + ".py", "r") as fin:
                    text = fin.read()
                frame.set_attributes("name_imf", value=value)
                frame.set_attributes("text_imf", value=text)

    def save_imf_handler(widget):
        #clear_output(wait=True)
        pyplot.close("all")
        imf_name = frame.get_attribute("name_imf", "value")
        
        if imf_name == "":
            print("Error: not IMF name given")
        else:
        
            if not os.path.isdir(custom_imf_dir):
                os.mkdir(custom_imf_dir)
                
            with open(custom_imf_dir + imf_name + ".py", "w") as fout:
                fout.write(frame.get_attribute("text_imf", "value"))
            print("Custom IMF saved to " + imf_name)
            
        frame.set_state_attribute('imf_type', options=['salpeter', 'chabrier', 'kroupa', 'alphaimf'] + list_custom_imf())

    def delete_imf_handler(widget):
        #clear_output(wait=True)
        pyplot.close("all")
        imf_name = frame.get_attribute("name_imf", "value")
        
        if imf_name == "":
            print("Error: not IMF name given")
        else:
        
            if os.path.isdir(custom_imf_dir):
                if os.path.isfile(custom_imf_dir + imf_name + ".py"):
                    os.remove(custom_imf_dir + imf_name + ".py")
                    frame.set_attributes("name_imf", value="")
                    frame.set_attributes("text_imf", value=default_custom_imf_text)
                    print("Custom IMF " + imf_name + " deleted.")
                else:
                    print("Custom IMF, " + imf_name + ", not found!")

        frame.set_state_attribute('imf_type', options=['salpeter', 'chabrier', 'kroupa', 'alphaimf'] + list_custom_imf())
            
    def test_imf_handler(widget):
        clear_output(wait=True)
        pyplot.close("all")
	display(frame._object_list["window"]) #CR

        imf_name = frame.get_attribute("name_imf", "value")
        
        if imf_name == "":
            print("No IMF name given!")
            return
        
        try:
            ci = load_source("custom_imf", custom_imf_dir + imf_name + ".py")
        except IOError:
            print("Failed to load " + imf_name + ", no IMF file found.")
            return

        mass_min = 0.0
        mass_max = 30.0
        
        xaxis = numpy.linspace(mass_min, mass_max, 1000)[1:]
        yaxis = [0 for x in xaxis]
        for i, x in enumerate(xaxis):
            yaxis[i] = ci.custom_imf(x)
        #close previous figures
        
        pyplot.plot(xaxis, numpy.log10(yaxis))
        pyplot.title("IMF file test: " + imf_name)
        pyplot.xlabel("mass [$M_{\odot}$]")
        pyplot.ylabel("IMF")
        pyplot.show()

        
    frame.set_state_callbacks("load_imf", load_imf_handler, attribute=None, type="on_click")
    frame.set_state_callbacks("list_imfs", sel_custom_imf)
    frame.set_state_callbacks("save_imf", save_imf_handler, attribute=None, type="on_click")
    frame.set_state_callbacks("delete_imf", delete_imf_handler, attribute=None, type="on_click")
    frame.set_state_callbacks("test_imf", test_imf_handler, attribute=None, type="on_click")
    
    
    frame.set_object("custom_imf_page", widgets.VBox())

    frame.set_object("load_save_imf_group", widgets.HBox())
    frame.set_object("load_imf", widgets.Button())
    frame.set_object("list_imfs", widgets.Dropdown())
    frame.set_object("name_imf", widgets.Text())
    frame.set_object("save_imf", widgets.Button())
    frame.set_object("delete_imf", widgets.Button())

    frame.set_object("text_imf", widgets.Textarea())
    
    frame.set_object("test_imf", widgets.Button())


    frame.set_state_attribute("get_table_page", visibility='visible')

    #frame.set_state_attribute("warning_msg", visibility='visible', value="<h3>Error: No simulation data!</h3>", **group_style)
    #frame.set_state_attribute("warning_msg", states_plot, visibility='hidden')
    
    frame.set_state_attribute("species_mult_group", states_sim_plot, visibility='visible', **group_style)
    frame.set_state_attribute("iso_or_elem2", visibility='visible', description="species type: ", options=["Elements", "Isotopes"], selected_label="Elements")
    frame.set_state_attribute("species_mult", visibility='visible', description="Element: ", options=elements_sel_mult, **text_box_style)

    frame.set_state_attribute("get_table", states_sim_plot, visibility='visible', description="Get table links", **button_style)
    frame.set_state_attribute("table_links", states_sim_plot, visibility='visible', value="", **group_style)
    
    def species_mult_handler(name, value):
        if "All" in value:
            iso_or_elem = frame.get_attribute("iso_or_elem2", "value")
            if iso_or_elem == "Elements":
                value = tuple(elements_all)
            elif iso_or_elem == "Isotopes":
                value = tuple(isotopes_all)
            frame.set_attributes("species_mult", value=value, selected_labels=value)
        frame.set_attributes("table_links", value="")

    def get_table_handler(widget):

        iso_or_elem = frame.get_attribute("iso_or_elem2", "value")
        species = list(frame.get_attribute("species_mult", "value"))
	print 'get_table_handler'
        runs = frame.get_state_data("runs")
        title = "<h3>Data table links:</h3>"
        html = title
        
        if not os.path.isdir("./evol_tables"):
            os.mkdir("./evol_tables")
        
        for data, name, Z, widget_name in runs:
            if frame.get_attribute(widget_name, "value"):
                file = "evol_tables/" + widget_name.replace("#", "") + "file.txt"
                if iso_or_elem == "Elements":
                    data.write_evol_table(species, [], file, "./")
                elif iso_or_elem == "Isotopes":
                    data.write_evol_table([], species, file, "./")
		print('create link')
                html = html + "<p><a href=\"" + file + "\" target=\"_blank\" download>" + name + "</a></p>\n"
        
        if html == title:
            html = ""
            print("No runs selected.")
        frame.set_attributes("table_links", value=html)
        #clear_output(wait=True)
        pyplot.close("all")
        
    frame.set_state_callbacks("species_mult", species_mult_handler)
    frame.set_state_callbacks("get_table", get_table_handler, attribute=None, type="on_click")

    frame.set_object("species_mult_group", widgets.VBox())
    frame.set_object("species_mult", widgets.SelectMultiple())
    frame.set_object("get_table_page", widgets.VBox())
    frame.set_object("get_table", widgets.Button())
    frame.set_object("table_links", widgets.HTML())

    ##start widget##
    frame.display_object("window")
