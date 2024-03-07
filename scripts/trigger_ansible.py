import os, sys
import requests
import jmespath

API_HEADERS = {"Content-Type": "application/json"}

def process_changes() -> set:
  raw_changed = [item for item in sys.argv[1].split('\n') if item.startswith('definitions/')]
  raw_all = [item for item in sys.argv[2].split('\n')][1:] # first element is the ls total

  changed = [item.split("/")[-1].split('.')[0] for item in raw_changed]
  all = map(lambda item: item.split(' ')[-1].split('.')[0], raw_all)
  ignored = [item + ".yml" for item in all if item and item not in changed]

  return changed, ignored

def launch_ansible(config, ignore_ees) -> None:
  body = {
    "extra_vars": {
      "ee_tag": config['commit'],
      "ees_ignore": ignore_ees
    }
  }
  headers = {
    "Authorization": "Bearer " + config['aap_token'],
    **API_HEADERS
  }
  url = f"https://{config['aap_host']}/api/v2/job_templates/{config['aap_jt_id']}/launch/"
  r = requests.post(url=url, json=body, headers=headers, verify=False)
  job_id = r.json().get('job', 'oops')
  print("Launched Ansible Job to build EEs: [version]=" + config['commit'])
  print("View job -> https://" + config['aap_host'] + '#/jobs/playbook/' + str(job_id))

def run(config):
  changed_ees, ignore_ees = process_changes()

  print("### CHANGED EEs ###")
  print(changed_ees)
  print("### IGNORE EEs ###")
  print(ignore_ees)

  if not len(changed_ees):
    print("No execution environment definitions require a new build, exiting...")
  else:
    launch_ansible(config, ignore_ees)

if __name__ == "__main__":
  config = {
    "commit": os.environ.get('CI_COMMIT_SHORT_SHA'),
    "aap_host": os.environ.get('AAP_HOST'),
    "aap_token": os.environ.get('AAP_TOKEN'),
    "aap_jt_id": os.environ.get('AAP_JOB_TEMPLATE_ID')
  }
  print(os.environ.get('AAP_HOST'))
  run(config)