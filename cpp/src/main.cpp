#include "GameManager.h"

int main(int argc, char *argv[]) {
  GameManager *g = NULL;
  try {
    g = new GameManager;
    return g->go();
  } catch (Ogre::Exception &e) {
#if OGRE_PLATFORM == OGRE_PLATFORM_WIN32
    MessageBoxA(NULL, e.getFullDescription().c_str(), "An exception has occured!", MB_OK | MB_ICONERROR | MB_TASKMODAL);
#else
  std::cerr << "An exception has occurred: " << e.getFullDescription();
#endif
  } catch (...) {
    std::cerr << "FATAL EXCEPTION check ogre.log";
  }
}
