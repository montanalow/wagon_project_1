#include <iostream>
#include <Ogre.h>
#include <OgreRenderSystem.h>

#include "GameManager.h"

//setup singleton
template<> GameManager* Ogre::Singleton<GameManager>::ms_Singleton = 0;
GameManager* GameManager::getSingletonPtr(void) {
  return ms_Singleton;
}
GameManager& GameManager::getSingleton(void) {  
  assert(ms_Singleton);
  return *ms_Singleton;  
}

GameManager::GameManager()
  : m_ogre(0)
  , m_render_system(0)
  , m_window(0)
  , m_main_viewport(0)
  , m_scene_mgr(0)
  , m_camera(0)
  , m_frame_timer(new Ogre::Timer())
  , m_update_timer(new Ogre::Timer())
{
  // init Ogre
  m_ogre = new Ogre::Root("etc/plugins.cfg", "");
  Ogre::LogManager::getSingletonPtr()->createLog("wagonz.log");
  const Ogre::RenderSystemList &renderers = m_ogre->getAvailableRenderers();
  Ogre::RenderSystemList::const_iterator it = renderers.begin();
  for(it; it != renderers.end(); ++it) {
    Ogre::RenderSystem *renderer = (*it);
    std::cout << "RENDER SYSTEM FOUND:" << renderer->getName() << std::endl;
  }
  // HACK: use the first renderer that was found
  m_render_system = *renderers.begin();
  //#m_render_system = m_ogre->getRenderSystemByName("Direct3D9 Rendering Subsystem");
  m_ogre->setRenderSystem(m_render_system);

  m_window = m_ogre->initialise(true);
  Ogre::WindowEventUtilities::addWindowEventListener(m_window, this);

  m_frame_timer->reset();
  m_update_timer->reset();
}

GameManager::~GameManager() {
  
}

void GameManager::render_frame() {
}
void GameManager::frame_started() {
}
void GameManager::frame_ended() {
}
int GameManager::go() {
  return 0;
}

// Ogre::WindowEventListener Methods
void GameManager::windowMoved(Ogre::RenderWindow* rw) {}
void GameManager::windowResized(Ogre::RenderWindow* rw) {}
void GameManager::windowClosed(Ogre::RenderWindow* rw) {}
void GameManager::windowFocusChange(Ogre::RenderWindow* rw) {}
