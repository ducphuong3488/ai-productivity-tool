import { Composition } from "remotion";
import { DURATION, FPS, H, W } from "./lib/time";
import { ThuongCon } from "./ThuongCon";

export const RemotionRoot: React.FC = () => {
  return (
    <Composition
      id="ThuongCon"
      component={ThuongCon}
      durationInFrames={Math.ceil(DURATION * FPS)}
      fps={FPS}
      width={W}
      height={H}
    />
  );
};
