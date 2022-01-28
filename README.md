# Apache-Airflow-Complete-Hands-On-Beginner-to-Advanced-Class

## Install Airflow on MacOS (Guide)
Follow these steps to install Airflow on your Mac.



1. Open a Terminal window.



2. Navigate to your Desktop in your Terminal. We are going to create a working directory here but you can create anywhere else in your file system if you like.

cd Desktop



3. Create a working directory here called airflow-tutorial.

mkdir airflow-tutorial



4. Change to airflow-tutorial directory in your Terminal.

cd airflow-tutorial



5. Create a virtual environment using conda (or any other tool). Install Python 3.7 in your virtual environment. I'm going to call the environment airflow-tutorial.

conda create --name airflow-tutorial python=3.7



6. Activate the virtual environment.

conda activate airflow-tutorial



7. Print the absolute path to our working directory by typing pwd.

I get /Users/alexaabbas/Desktop/airflow-tutorial but you might get something different. Copy this path.



8. Set the path as the AIRFLOW_HOME environment variable. Note that you have to do this every time you open a new Terminal window and wish to use Airflow CLI. Alternatively you can set a permanent environment variable in your bash_profile.

export AIRFLOW_HOME=/Users/nivedita/Desktop/airflow-tutorial

By default airflow uses ~/airflow as it's AIRFLOW_HOME directory. We can overwrite this by setting a different path. Airflow will initialise the airflow.cfg file here along with the logs folder. We'll store our dags and plugins in this directory.



9. Install Airflow 1.10.10 + extras using pip.

pip install apache-airflow[gcp,statsd,sentry]==1.10.10

If you’re using zsh like me then you need to put apache-airflow[gcp,statsd,sentry] in quotes as shown below.

pip install 'apache-airflow[gcp,statsd,sentry]'==1.10.10



10. Install extra packages that we’ll need later.

pip install cryptography==2.9.2

pip install pyspark==2.4.5



11. Validate your Airflow installation.

airflow version

This should print 1.10.10.

If you have installed Airflow before you might get a DeprecationWarning about having multiple airflow.cfg files but that’s okay as long as you set the correct AIRFLOW_HOME environment variable in your Terminal.


## Run Airflow locally

1. activate virtual environment
   
   conda activate airflow-tutorial


2. Check Airflow Home Path

export AIRFLOW_HOME="/Users/nivedita/Desktop/airflow-tutorial"

echo $AIRFLOW_HOME


3. Initialize the airflow  database which will create the table necessary for airflow dags and status

airflow db init 


4. Run Webserver

airflow webserver


5. Run Scheduler parallel in another new tab of command line

airflow scheduler


