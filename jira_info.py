from jira import JIRA
import config


def jira_info(login, password):
    auth_jira2 = JIRA(server="https://jira2.s7.aero", auth=(login, password))
    auth_jira = JIRA(server="https://jira.s7.aero", auth=(login, password))
    jira_search = auth_jira.search_issues('assignee in ("Администраторы VSM", "ССП операторы") AND resolution = '
                                          'Unresolved order by updated DESC')
    jira2_search = auth_jira2.search_issues(
        'resolution = Unresolved AND assignee in (sysadm.operators, "ССП операторы") order by updated DESC')
    jira2_test = auth_jira2.search_issues('assignee = currentUser() AND resolution = Unresolved order by updated DESC')
    jira_information = []
    for jira123 in jira2_test:
        jira_information.append(f"\vJIRA\n"
                                f"------------------------------------------------------------------\n"
                                f"Тема: {jira123.fields.summary}\n"
                                f"Описание: {jira123.fields.description}\n"
                                f"Испольнитель: {jira123.fields.assignee}\n\n"
                                )
    return jira_information
# jira_search = [1, 2, 3]
# jira2_search = [4, 5 ,6]

# for jira in jira2_search + jira_search + jira_test:
#     print(jira)
