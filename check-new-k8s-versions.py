import sys
import requests
import json
from natsort import natsorted
from natsort import natsort_keygen
import pprint

natsort_key = natsort_keygen()

def get_previous_key(dic, current_key):
    l=list(dic) # convert the dict keys to a list

    try:
        previous_key=l[l.index(current_key) - 1]
    except (ValueError, IndexError):
        return False
    return previous_key

dev_data = json.load(open('data/data.json'))
release_data_url = f"https://releases.rancher.com/kontainer-driver-metadata/release-v2.6/data.json"
response = requests.get(release_data_url)
response.raise_for_status()
release_data = response.json()

release_versions = release_data.get('K8sVersionRKESystemImages', {}).keys()
release_keys = list(release_versions)
natsorted(release_keys) == sorted(release_keys, key=natsort_key)
release_keys.sort(key=natsort_key)

dev_versions = dev_data.get('K8sVersionRKESystemImages', {}).keys()
dev_versions_map = dev_data.get('K8sVersionRKESystemImages', {})
dev_keys = list(dev_versions)
natsorted(dev_keys) == sorted(dev_keys, key=natsort_key)
dev_keys.sort(key=natsort_key)

diff = list(set(dev_keys) - set(release_keys))
if len(diff) == 0:
    print("No new versions found")

print("New k8s versions found:")

for new_version in diff:
    print(f"- `{new_version}`")


pp = pprint.PrettyPrinter(indent=4)

for new_version in diff:
    previous_version = get_previous_key(sorted(dev_versions_map, key=natsort_key), new_version)
    print("\n---")
    print("Diff:")
    print(f"- `{new_version}` (newly added)")
    print(f"- `{previous_version}` (previous semver version)")

    current_images = dev_versions_map[new_version]
    previous_images = dev_versions_map[previous_version]

    current_set = set(current_images.items())
    previous_set = set(previous_images.items())

    print("```")
    #pp.pprint(current_set - previous_set)
    pretty = json.dumps(list(current_set - previous_set), indent=4)
    print(pretty)
    print("```")
