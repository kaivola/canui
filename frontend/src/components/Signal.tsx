import { Card, Flex, Slider, Switch, Text } from "@radix-ui/themes";
import type { Signal as SignalType } from "../types/schema";
import { memo } from "react";

interface Props {
  signal: SignalType;
  onChange: (signalName: string, value: number) => void;
}

export const Signal = memo(({ signal, onChange }: Props) => {
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
            onValueChange={(e) => onChange(signal.name, e[0])}
            min={signal.nominal_min ?? 0}
            max={signal.nominal_max ?? Number.MAX_SAFE_INTEGER}
            step={signal.step}
          />
        ) : (
          <Switch onCheckedChange={val => onChange(signal.name, val ? 1 : 0)} />
        )}
      </Flex>
    </Card>
  );
});
