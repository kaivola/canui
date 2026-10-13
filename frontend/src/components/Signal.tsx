import { Card, Flex, Slider, Switch, Text } from "@radix-ui/themes";
import type { Signal as SignalType } from "../types/schema";

interface Props {
  signal: SignalType;
  onChange: (value: number) => void;
}

export const Signal = ({ signal, onChange }: Props) => {
  return (
    <Card mb={"4"}>
      <Flex direction={"column"} gap={"6"}>
        <Flex direction={"column"}>
          <Flex justify={"between"} align={"center"}>
            <Text size={"4"}>{signal.displayName}</Text>
            <Text size={"7"}>{signal.value}</Text>
          </Flex>
          <Text style={{ color: 'var(--gray-10)' }}>{signal.comment}</Text>
        </Flex>
        {signal.length > 1 ? (
          <Slider
            defaultValue={[signal.value ?? 0]}
            onValueChange={(e) => onChange(e[0])}
            min={signal.min_value ?? 0}
            max={signal.max_value ?? Number.MAX_SAFE_INTEGER}
          />
        ) : (
          <Switch onCheckedChange={val => onChange(val ? 1 : 0)} />
        )}
      </Flex>
    </Card>
  );
};
