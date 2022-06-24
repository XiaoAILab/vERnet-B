source /data1/dragon/miniconda2/etc/profile.d/conda.sh

protein_HGVS=$1
variant_type=$2
ul_id=$3
dir_path=/data1/lc/vEPnet_web/

if [ ${variant_type} -eq 1 ];then
    dir_path=${dir_path}BRCA1/
fi

fasta_path=${dir_path}fastas/${protein_HGVS}.fasta
pdb_dir=${dir_path}pdbs
pdb_path=${pdb_dir}/${protein_HGVS}.pdb
ea_path=${dir_path}eas/${protein_HGVS}_h_nrint.ea
mat_path=${dir_path}mats/${protein_HGVS}.mat
result_path=${dir_path}results/${protein_HGVS}.txt


conda activate af2

/data1/dragon/miniconda2/envs/pymol/bin/python3.6 /data1/lc/vEPnet_web/Source/HGVS_to_fasta.py ${fasta_path} ${protein_HGVS} ${variant_type} ${result_path}

if [ $? -eq 2 ];then
    echo "vEPnet: predict_Ensemble successed"
    exit 1
fi

if [ ! -f "${fasta_path}" ];then
    echo "vEPnet: HGVS_to_fasta failed"
    exit 1
else
    echo fasta_path:${fasta_path}
    echo "vEPnet: HGVS_to_fasta successed"
fi


if [ ! -f "${pdb_path}" ];then

    process_num=`ps -ef | grep run_alphafold | grep -v grep | wc -l | awk '{print $1}'`

    while [ ${process_num} -gt 2 ]
    do
        echo "vEPnet: Waiting 300 seconds"
        sleep 300
        process_num=`ps -ef | grep run_alphafold | grep -v grep | wc -l | awk '{print $1}'`
    done

    /data1/dragon/miniconda2/envs/af2/bin/python3.8 /data1/lc/alphafold-main/run_alphafold.py --fasta_paths=${fasta_path} --output_dir=${pdb_dir}

    mv ${pdb_dir}/${protein_HGVS}/ranked_0.pdb ${pdb_path}
    rm -rf ${pdb_dir}/${protein_HGVS}

    if [ ! -f "${pdb_path}" ];then
        echo "vEPnet: run_alphafold failed"
        exit 1
    else
        echo pdb_path:${pdb_path}
        echo "vEPnet: run_alphafold successed"
    fi
else
    echo pdb_path:${pdb_path}
    echo "vEPnet: .pdb have been existed"
fi

conda activate RINerator
export PATH=/data1/lc/reduce-master/reduce_src/:$PATH
export PATH=/data1/lc/probe-master/:$PATH

/data1/dragon/miniconda2/envs/RINerator/bin/python2.7 /data1/lc/RINerator_V0.5.1/Source/get_chains.py ${pdb_path} ${dir_path}RINerator/ /data1/lc/RINerator_V0.5.1/Test/INPUT/chains_1hiv_A.txt

mv ${dir_path}RINerator/${protein_HGVS}_h_nrint.ea ${ea_path}
rm -rf ${dir_path}RINerator/${protein_HGVS}*

if [ ! -f "${ea_path}" ];then
    echo "vEPnet: RINerator failed"
    exit 1
else
    echo ea_path:${ea_path}
    echo "vEPnet: RINerator successed"
fi

conda activate af2
/data1/dragon/miniconda2/envs/af2/bin/python3.8 /data1/lc/vEPnet_web/Source/generate_mat.py ${ea_path} ${mat_path} ${variant_type}

rm -rf ${ea_path}

if [ ! -f "${mat_path}" ];then
    echo "vEPnet: generate_mat failed"
    exit 1
else
    echo mat_path:${mat_path}
    echo "vEPnet: generate_mat successed"
fi

/data1/dragon/miniconda2/envs/tensorflow/bin/python /data1/lc/vEPnet_web/Source/Basic_CNNs_TensorFlow2-master_BRCT/predict_Ensemble.py 1 ${mat_path} ${result_path} ${protein_HGVS}

# rm -rf ${mat_path}

# if [ $? -eq 1 ];then
#     echo "vEPnet: predict_Ensemble failed"
#     exit 1
# else
#     echo "vEPnet: predict_Ensemble successed"
# fi
if [ ! -f "${result_path}" ];then
    echo "vEPnet: predict_Ensemble failed"
    exit 1
else
    echo result_path:${result_path}
    echo "vEPnet: predict_Ensemble successed"
    rm -rf ${result_path}
fi
