import React from 'react';
import {useCurrentFrame} from 'remotion';
import {getSceneAtFrame} from './timeline';
import {Exposure} from './scenes/Exposure';
import {Intent} from './scenes/Intent';
import {Fhe} from './scenes/Fhe';
import {Zk} from './scenes/Zk';
import {Notes} from './scenes/Notes';
import {Boundaries} from './scenes/Boundaries';
import {Brand} from './scenes/Brand';

/**
 * Seven illustrated scenes. Only the active scene renders, so nothing off-stage can leak into captions.
 * Local time is global frame minus the scene start; every visible value is a pure function of it.
 * The wrapper owns the full-bleed background, captions, fonts and the y=880 clip.
 */
export const Film:React.FC=()=>{
  const frame=useCurrentFrame();
  const scene=getSceneAtFrame(frame);
  const f=frame-scene.startFrame;
  const Scene={exposure:Exposure,intent:Intent,fhe:Fhe,zk:Zk,notes:Notes,boundaries:Boundaries,brand:Brand}[scene.id as 'exposure'|'intent'|'fhe'|'zk'|'notes'|'boundaries'|'brand'];
  return <div style={{position:'absolute',left:0,top:0,width:1920,height:1080}}><Scene f={f}/></div>;
};
