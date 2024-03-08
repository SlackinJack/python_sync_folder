import subprocess

# first create a config.cfg:
# (this file will not be included, for obvious reasons)
#
# ADDRESS=localhost
# PORT=22
# USERNAME=username
# PASSWORD=password
# REMOTE_WORKING_DIR=/home/username/Desktop/
# REMOTE_TARGET_DIR=remote_folder


errored = False
def printErrorsIfPresent(errorsIn):
    if len(errorsIn) > 0:
        print(errorsIn)
        global errored
        errored = True
    return


fileConfiguration = open("config.cfg", "r")
configuration = fileConfiguration.read()
fileConfiguration.close()
config = dict()
for line in configuration.split("\n"):
    if len(line) > 0 and not line.startswith("#"):
        l = line.split("=")
        config[l[0]] = l[1]


# delete the folder we are syncing on CLIENT
subprocess.run(["rm", "-r", config["REMOTE_TARGET_DIR"]])

# pull folder from REMOTE
printErrorsIfPresent(
    subprocess.run(
        [
            "sshpass", "-p", config["PASSWORD"],
            "scp", "-r", "-P", config["PORT"], config["USERNAME"] + "@" + config["ADDRESS"] + ":" + config["REMOTE_WORKING_DIR"] + config["REMOTE_TARGET_DIR"], "."
        ],
        capture_output = True,
        text = True
    ).stderr
)


if not errored:
    input("""-------------------------------------

Directory '{}' has been downloaded.
Press ENTER to upload the directory.

-------------------------------------""".format(config["REMOTE_TARGET_DIR"]))
    
    # delete folder from REMOTE
    subprocess.run(
        [
            "sshpass", "-p", config["PASSWORD"],
            "ssh", "-p", config["PORT"], config["USERNAME"] + "@" + config["ADDRESS"], "rm", "-r", config["REMOTE_WORKING_DIR"] + config["REMOTE_TARGET_DIR"]
        ]
    )
    
    # push folder to REMOTE
    printErrorsIfPresent(
        subprocess.run(
            [
                "sshpass", "-p", config["PASSWORD"],
                "scp", "-r", "-P", config["PORT"], config["REMOTE_TARGET_DIR"], config["USERNAME"] + "@" + config["ADDRESS"] + ":" + config["REMOTE_WORKING_DIR"]
            ],
            capture_output = True,
            text = True
        ).stderr
    )
    
    
    if not errored:
        print("Your files have been synced to the remote directory.")
        
        # delete folder from CLIENT
        if input("Do you want to delete the local copy? (y/n): ").lower() == "y":
            subprocess.run(["rm", "-r", config["REMOTE_TARGET_DIR"]])

