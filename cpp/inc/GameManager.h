#ifndef __GAME_MANAGER_H
#define __GAME_MANAGER_H

#include <Ogre.h>
#include <OgreSingleton.h>

class GameManager :
  public Ogre::Singleton<GameManager>,
  public Ogre::WindowEventListener
{
public:
  GameManager();
  ~GameManager();

  void render_frame();
  void frame_started();
  void frame_ended();

  int go();

  // Ogre::Singleton
  static GameManager& getSingleton(void);
  static GameManager* getSingletonPtr(void);

  // Ogre::WindowEventListener Methods
  void windowMoved(Ogre::RenderWindow* rw);
  void windowResized(Ogre::RenderWindow* rw);
  void windowClosed(Ogre::RenderWindow* rw);
  void windowFocusChange(Ogre::RenderWindow* rw);

private:
  Ogre::Root *m_ogre;
  Ogre::RenderSystem *m_render_system;
  Ogre::Camera *m_camera;
  Ogre::SceneManager *m_scene_mgr;
  Ogre::Timer *m_frame_timer, *m_update_timer;
  Ogre::RenderWindow *m_window;
  Ogre::Viewport *m_main_viewport;
};

#endif // __GAME_MANAGER_H
