from workflow import Workflow3
from jenkins.jenkins_interface import JenkinsInterface, NoJobsFound


def main(wf):
    wf.setvar('WF_USERNAME', 'jenkins')
    command = wf.args[0]
    query = wf.args[1] if len(wf.args) > 1 else None
    interface = JenkinsInterface(wf)

    options = {
        'set_url': interface.set_jenkins_url,
        'login': interface.set_login,
        'clear_login': interface.clear_login,
        'failing': interface.get_failed_jobs,
        'building': interface.get_building_jobs,
        'all': interface.get_all_jobs
    }

    try:
        jobs = options[command](query)

        if not query:
            wf.add_item("Open Jenkins",
                        arg=interface.get_jenkins_url(),
                        valid=True)

        for job in jobs:
            item = wf.add_item(title=job.name,
                        subtitle=job.build_infos,
                        arg=job.last_build_url if command == 'building' else job.url,
                        valid=True,
                        icon=job.image)

            item.add_modifier(
                key='shift',
                subtitle='Open console',
                arg=job.last_build_url,
                valid=bool(job.last_build_url)
            )

    except NoJobsFound:
        wf.logger.debug("Could not find any jobs for instance: %s",
                        wf.settings['jenkins_url'])
        wf.add_item("Error: No jobs found")

    wf.send_feedback()


if __name__ == '__main__':  # pragma: no cover
    Workflow3().run(main)
