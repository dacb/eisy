"""
WIP for testing data Import, Formatting, and then Export to SQL and/or other


Section 0: Importer Configuration File
--------------------------------------
* new_config_import()   Takes an optional/default file path and writes a new
                        configuration file in that location, with additional
                        optional inputs. The basic config file format is
                        HARD-CODED here, and can be edited as we want.
                        Optionally (default TRUE) will save the new file

* get_config_import()   Takes a config file path and loads the file if exists

* set_config_import()   Takes a config file path and dictionary of changes.
                        Either uploads the existing file in that path, or
                        creates a new one using the above functions.
                        Changes (and/or adds, optionally) the keys given,
                        and re-saves the config file.

NOTE:   To make use of Configuration codes, will call set_config_import()
        BEFORE we define other functions, so that their DEFAULT Values
        can be set according to the configuration files.
        This may or may not be kosher... I'm honestly not sure.


Section 1: Getting List of Files
--------------------------------
* get_file_list()       Takes a directory and filter parameters.
                        Returns atuple of all files in the directory
                        that match the filter parameters.

* check_dir_path()      Takes a directory and a single "AND-filter."
                        Passes if a certain number (parameter n) of files in
                        the directory contain the filter parameter.

* ask_file_list()       Simpler solution. Uses tkinter window to ask user to
                        multiselect files to be imported.


Section 2: Import F-Series Data Files (and Process Meta-Data)
-------------------------------------------------------------
* parse_fname_meta()    Takes a file name and separates out any/all metadata
                        of interest (Serial ID, Source, NN Tags)

* read_fseries_data()   Takes a file name, expected metadata information, and
                        some interaction parameters (?)
                        Reads the file,









"""
# ----------------------------------------------------------------------------
# --- HARD - CODING SECTION --------------------------------------------------
# ----------------------------------------------------------------------------
config_file_location = "config/config_importer.yaml"







"""
-------------------------------------------------------------------------------
-------------------------------------------------------------------------------
---SECTION 0 : Configuration Files---------------------------------------------
-------------------------------------------------------------------------------
-------------------------------------------------------------------------------
"""


def new_config_import(config_file="config/config_importer.yaml",
                      save=True, interact=False, popup=False, **change):
    """
    This function will set up a config file for data importing,
    and can be customized in many ways, depending on user interest.

    INPUT:
        config_file     : String where we can save the file, if desired.
                          if file already exists, will raise error.

        save            : Boolean, whether or not to save this file.
                          either way will return a config dictionary

        interact        : Boolean, whether to ask the user to manually submit
                          additional values to the dictionary.

        popup           : Boolean, whether interactions should use tkinter
                           input windows, or ask for input in the kernel.

        **change        : **KWARGS - User can input additional elements which
                          will be added to the dictionary

    RETURN:
        config          : Dictionary (or dataframe? pandas series?) in config

    ACTIONS:
        * Optional request for any additional arguments
        * Optional save-file (if SAVE)

    NOTE: FUNCTION IS WORK-IN-PROGRESS. For MAIN USE-CASE, currently
            require user input to be hard-coded in the initial "config"
            dictionary below. It's also an open question whether to save
            as CSV file or whether to learn/use YAML'
    """
    import yaml
    from datetime import datetime
    import os.path
    config_dir = os.path.dirname(config_file)
    config = {
            "data_dir": "data/simulation/sim_data",
            "config_created": str(datetime.now()),
            "config_updated": None,
            "file_type": ".csv",  # just to check that the edit works
            "header_meta": {
                    "date_run": "Date:",
                    "serial_n": "Serial number:",
                    "d_source": "Data Source:",
                    "circuit_str": "Cirucit type:",
                    "circuit_detail": "Circuit elements:"
                    },
            "header_end_str": "---",
            "fdata_delim": ",",
            "fdata_head": {
                    "freq_hz":   "freq [Hz]",
                    "real_ohm":  "Re_Z [Ohm]",
                    "imag_ohm":  "Im_Z [Ohm]",
                    "totl_ohm":  "|Z| [Ohm]",
                    "phase_rad": "phase_angle [rad]",
                    }
              }
    if change:
        # Handle arguments passed directly into funciton:
        # Probably overwrite if key exists, otherwise simply
        # add to dictionary?
        print("Work in Progress. Will execute kwargs another time")
        pass

    if interact:
        # Did the user ask for an interaction? If so, how?
        if popup:
            # If the user wants a tkinter window to ask for
            # what arguments they want, then give them that?
            import tkinter
            change_interact = ""  # WIP, leave empty
        else:
            # If no popup windows, then ask in command line
            print("Please Input Config Parameters. Leave blank to finish")
            key = 'init'  # Counter (to avoid infinite loop?)
            change_str = 'test'
            while key and change_str:
                print("\n")
                key = input("Input Key:    ")
                change_str = input("Input Value:  ")
                if key and change_str:
                    # If you passed two arguments, assign the value to the key
                    # in the config dictionary
                    config[key] = change_str

    if save:
        # If instructions are to save the new config file,
        # We will use dump YAML, as suggested in class
        # But first check that the path to save exists

        if os.path.isdir(config_dir):
            pass
        else:
            # Create directory if doesn't exist
            os.mkdir(config_dir)

        # Now, save the file using yaml
        f = open(config_file, "w+")
        yaml.dump(config, f)
        f.truncate()
        f.close()

    return config


def get_config_import(config_file="config/config_importer.yaml",
                      interact=False):
    """
    Simple import script, to load the YAML configuration file.
    So far it just checks that the file exists, and if it does it loads it.
    IF doesn't exist, either raises error or uses a TKinter window to ask.

    Future WIP: Test Checks to make sure that the file contains the needed
                configuration parameters that we use in our other programs.
                Namely:
                * file_dir : The directory to default load data files from
                *
                *
    """
    import yaml
    import os.path
    import tkinter
    from tkinter.filedialog import askdirectory
    if os.path.isfile(config_file):
        pass
    else:
        if interact:
            print("No Config Found! Select Config File:")
            root = tkinter.Tk()
            root.lift()
            root.focus_force()
            config_file = askdirectory(parent=root,
                                       title="Select Import Config",
                                       initialdir=os.path.abspath(config_file)
                                       )
            root.destroy()
        else:
            raise AssertionError("No Config Found at : " + config_file + '\n' +
                                 "Try Again with a different file path!")

    f = open(config_file, "r")
    config = yaml.safe_load(f)
    f.close()
    return config


def set_config_import(config_file="config/config_importer.yaml",
                      change={"file_type": ".csv"}, add_new=False):
    """
    Create or Modify configuration file, used to pass new defaults
    Will import and parse the file if it exists.
    Otherwise it starts from scratch, and saves the file afterwards.
    INPUT:
        config_file :   [str] The file path and file to read as the importer.
                        In a meta-sense, this default should probably be
                        UNIFIED throughout the document. IF SO, perhaps
                        I should define this globablly at the top.
                        (Also would be easier to hard-code for users)

        change :        [dict] Open ended... A ldict of keys to edit in the
                        config file. Anything put here will overwrite the
                        existing config dictionary for that item.
                        We have the default filetype:csv here as an example

        add_new :       [BOOL] how to handle keys given to "Change" that are
                        not in the existing config file. If TRUE, will add
                        new keys to the end of the config. if FALSE, will
                        raise assertionerror - key not found.

    """
    import os.path
    from datetime import datetime
    import yaml

    if os.path.isfile(config_file):
        # Import existing Config, to be edited
        print("Importer Configuration found!")
        config = get_config_import(config_file)
    else:
        # CREATE NEW CONFIG DICT FROM SCRATCH
        print("Importer Configuration Not found! \nCreating New One...")
        config = new_config_import(save=False, interact=False)

    # Now go through every key in the change dictionary and update config
    change_keys = change.keys()
    for key in change_keys:
        if key not in config.keys():
            # How to handle a "Change" entry that isn't already in the config??
            if add_new:
                config[key] = change[key]
            else:
                raise AssertionError("Key <" + str(key) +
                                     "> is not in Config file")
        else:
            config[key] = change[key]

    # Always update config_updated timestamp, right before saving
    config["config_updated"] = str(datetime.now())
    # save_config = pd.DataFrame.from_dict(data=config) # This seems broken?
    # Not sure why the dataframe idea wasn't working, however I think we can
    #    just leave things as the dictionary.

    f = open(config_file, 'w+')
    yaml.dump(config, f)      # Save and overwrite config file
    f.truncate()              # Eliminates extra lines if file got shorter
    f.close()
    return config


"""
-------------------------------------------------------------------------------
-------------------------------------------------------------------------------
---SECTION 1 : Files to Import List   -----------------------------------------
-------------------------------------------------------------------------------
-------------------------------------------------------------------------------
"""


def get_file_list(dir_path="data/simulation/sim_data/",
                  str_has=['sim'], str_inc=['0001', '0002'], ftype='.csv',
                  interact=True):
    """
    Get a list of file paths to open, which fulfill certain criteria.
    (Alternative to single/multiselect File Dialog, or hard-coded file names
        INPUTS:
            * Path to check initially.
                (hard-coded default for now. can we globally config?)
            * Basic filter parameters, defaults just for testing now.
                str_has: AND filter (Must contain all in list)
                str_inc: OR  filter (Must contain at least one)
            * File type to check for. Default csv
            * whether to use file dialogs if the path fails, or just error out.
        OUTPUTS:
            * TUPLE of file names that pass the tests (built as list)
            * Final (successful) directory path used. (from cwd, or from base)

    """
    import os.path
    from os import listdir
    import tkinter
    from tkinter.filedialog import askdirectory
    root = tkinter.Tk()  # this will help control file dialog boxes!

    # Check if the path specified includes at least 1 file of the file type
    success, err_msg = check_dir_path(dir_path, [ftype], 1, False)

    while not success and len(dir_path):
        # If the "default" directory failed the check,
        # Either raise that error, or ask for a different directory!
        # (Will exit If you X out of the dialog, to avoid getting stuck)
        if interact:
            root.lift()
            root.focus_force()
            dir_path = askdirectory(parent=root, title=err_msg,
                                    initialdir=dir_path)
            success, err_msg = check_dir_path(dir_path, [ftype], 1, False)
        else:
            root.destroy
            raise AssertionError(err_msg)
    if not len(dir_path):
        root.destroy()
        raise AssertionError("You Closed the Dialog Window Without a Folder!")
    root.destroy()

    """
    If we've gotten this far, we found files!
    So now, we will filter the list based on the parameters given, and return
    the result as a file list to open.
    """
    full_dir = listdir(dir_path)
    files_wanted = []
    for file in full_dir:
        # For each file, decide if it passes
        for str_AND in str_has:
            # IF any of these fail, ignore the file.
            if str_AND in file:
                pass
            else:
                break
        else:
            # Only does this if all "Required" strings pass
            for str_OR in str_inc:
                # If ANY string is found in the file,
                # Add it to the list and then go to next file
                if str_OR in file:
                    files_wanted.append(os.path.join(dir_path, file))
                    break
                else:
                    pass
    return tuple(files_wanted), dir_path


def check_dir_path(dir_path, files_contain=['.csv'], n_required=1,
                   raise_err=False):
    """
    Check if a directory contains the files you want:
        INPUTS:
            * Path to check (required)
            * LIST of strings to check. Files must contain ALL strings to pass.
                (Default is set to look for .csv)
            * Number of successful files required to pass the test
                (Default is 1 file)
            * Failure Handling. whether to Return Failure or raise an Error.
                (Default is FALSE, which will not raise errors.)
        OUTPUTS:
            * BOOLEAN (T/F), did we find all the required files?
            * Error Message, to use in selecting a folder if we failed.
    """
    import os.path
    from os import listdir
    if os.path.isdir(dir_path):
        # First confirm that it's a directory, otherwise fail
        file_list = listdir(dir_path)
        if len(file_list) == 0:
            if raise_err:
                raise AssertionError("That Directory is Empty")
            else:
                return False, "That Directory is Empty!"
        else:
            files_found = 0
        for file in file_list:
            # Search each file name
            for str_required in files_contain:
                # To succeed, must have ALL strings in the list
                if str_required in file:
                    # If this string is in the name
                    pass  # Check the next string required
                else:
                    break  # Break out of this loop (try next file?)
            else:
                # This FOR-ELSE means the file name passed the test!
                files_found += 1  # Add 1 to found_files
                if files_found >= n_required:
                    return True, "At least "+str(n_required)+" files passed!!"
        else:
            # This FOR-ELSE means that no files passed!
            if raise_err:
                raise AssertionError(str(files_found) +
                                     " Files Passed. Needed " +
                                     str(n_required) + ".")
            else:
                return False, str(str(files_found) + " Files Passed. Needed " +
                                  str(n_required) + ".")
    else:
        if raise_err:
            raise AssertionError("This is not a Directory!")
        return False, "This Is Not a Directory"
    return False, "Something Else went Wrong? Debug..."


def ask_file_list():
    """
    Alternative to get_file_list, just makes a tkinter window and asks the user
    to select the files. Written easiy so we don't have to remember tkinter
    """
    import os.path
    import tkinter
    from tkinter.filedialog import askopenfilenames
    root = tkinter.Tk()
    files_list = askopenfilenames(multiple=True)
    root.destroy()

    return files_list, os.path.abspath(files_list[0])

