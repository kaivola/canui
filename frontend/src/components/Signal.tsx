import { Card, Flex, Slider, Switch, Text } from "@radix-ui/themes";
import type { Signal as SignalType } from "../types/schema";

interface Props {
  signal: SignalType;
  onChange: (value: number) => void;
}

export const Signal = ({ signal, onChange }: Props) => {
  return (
    <Card>
      <Flex direction={'column'} gap={"4"}>
        <Text>{signal.name}</Text>
        {signal.length > 1 ? (
          <Slider
            onValueChange={(e) => onChange(e[0])}
            min={signal.min_value ?? 0}
            max={signal.max_value ?? Number.MAX_SAFE_INTEGER}
          />
        ) : (
          <Switch onCheckedChange={Number} />
        )}
      </Flex>
    </Card>
  );
};
