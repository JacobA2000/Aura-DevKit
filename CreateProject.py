from GeneralHandlers import ConfigHandler, GitHandler

GitHandler.CheckAndGetGitConfig()
GitHandler.CreateRepo("test", False)