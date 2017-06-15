# you must run this
# arg1 is the working directory of your code
# arg2 is the full path of your VirtualEnvs/qbpython folder
# args 3 through n are that modules arguments
# example: (run from your-qbpython-workspace/caponelockbox/caponelockbox)
# sh ../../pypostgres/pypg/run_it.sh /users/bperlman1/Virtualenvs/qbpython  ./ run_all_bank_stuff_daily.py -write_to_db true -bai2_text_file "${bai_txt_file_full_path}" -bank_statement_table developer.bank_statements_temp -sql_migrate_procedure developer.migrate_single_payment_deposits -db_csv_path "../../dbqbsync/dbqbsync/db_jona.csv"

initdir=$(pwd)
shcmd="$0"
virenv_qbpython="$1"
workingdir="$2"


# STEP 2: establish full path of working directory in next 3 lines
cd ${workingdir}
workingdir=$(pwd)

# STEP3: execute source bin/activate
cd ${virenv_qbpython}
source bin/activate

# STEP4: go back to 
cd ${workingdir}

# STEP 1: get full path of run_it.sh folder,which is where run_it.py will be
runitdir=$(dirname ${shcmd})
runitdir=$(cd ${initdir}/${runitdir};pwd)
#cd ${initdir}

echo "working dir is ${workingdir} "
echo "run_it.py dir is ${runitdir} "
echo "virtual env dir is ${virenv_qbpython} "

# STEP5: get qbpython workspace folder full path
qbpython_workspace_dir="${workingdir}/../../"

# STEP6: run run_it.py
python  ${runitdir}/run_it.py "${qbpython_workspace_dir}" ${@:3} 
 