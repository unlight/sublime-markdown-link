workflow "Test, Publish" {
  resolves = ["Publish"]
  on = "push"
}

action "Test" {
    env = {
        PACKAGE = "MarkdownLink"
        SUBLIME_TEXT_VERSION = "3"
    }
    uses = "./"
    runs = "sh test.sh"
}

action "Master" {
  needs = ["Test"]
  uses = "actions/bin/filter@master"
  args = "branch master"
}

action "Publish" {
  needs = ["Master"]
  uses = "docker://node:12"
  runs = "npm install && npx semantic release -d"
  secrets = ["GITHUB_TOKEN"]
}
